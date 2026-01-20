"""ChromaDB Vector Store management"""
import os
from pathlib import Path
from typing import List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import settings
from .embeddings import get_embeddings


class VectorStoreManager:
    """Manages ChromaDB vector store operations"""

    def __init__(self):
        self.embeddings = get_embeddings()
        self.collection_name = settings.chroma.collection_name
        self._vectorstore: Optional[Chroma] = None
        self._client: Optional[chromadb.HttpClient] = None

    def _get_client(self) -> chromadb.HttpClient:
        """Get or create ChromaDB client"""
        if self._client is None:
            # Parse host and port from settings
            host_url = settings.chroma.host
            if host_url.startswith("http://"):
                host_url = host_url[7:]
            elif host_url.startswith("https://"):
                host_url = host_url[8:]

            if ":" in host_url:
                host, port = host_url.split(":")
                port = int(port)
            else:
                host = host_url
                port = 8000

            self._client = chromadb.HttpClient(
                host=host,
                port=port,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
        return self._client

    def get_vectorstore(self) -> Chroma:
        """Get or create the vector store"""
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                client=self._get_client(),
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
        return self._vectorstore

    def add_documents(self, documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> int:
        """
        Add documents to the vector store with chunking

        Args:
            documents: List of Document objects to add
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            Number of chunks added
        """
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

        chunks = text_splitter.split_documents(documents)

        # Add to vector store
        vectorstore = self.get_vectorstore()
        vectorstore.add_documents(chunks)

        return len(chunks)

    def load_markdown_documents(self, directory: Path) -> List[Document]:
        """
        Load markdown documents from a directory

        Args:
            directory: Path to directory containing markdown files

        Returns:
            List of Document objects
        """
        documents = []

        if not directory.exists():
            return documents

        for md_file in directory.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")

                # Extract metadata from path
                relative_path = md_file.relative_to(directory)
                parts = relative_path.parts

                metadata = {
                    "source": str(md_file),
                    "filename": md_file.name,
                    "relative_path": str(relative_path)
                }

                # Try to extract week/day info from path
                for part in parts:
                    if part.lower().startswith("week"):
                        metadata["week"] = part
                    elif part.lower().startswith("day"):
                        metadata["day"] = part

                documents.append(Document(page_content=content, metadata=metadata))

            except Exception as e:
                print(f"Error loading {md_file}: {e}")

        return documents

    def ingest_documents(self, directory: Optional[Path] = None) -> dict:
        """
        Ingest all markdown documents from the data directory

        Args:
            directory: Optional custom directory path

        Returns:
            Dict with ingestion statistics
        """
        if directory is None:
            directory = settings.paths.data_dir

        documents = self.load_markdown_documents(directory)

        if not documents:
            return {"status": "no_documents", "count": 0}

        chunks_count = self.add_documents(documents)

        return {
            "status": "success",
            "documents_loaded": len(documents),
            "chunks_created": chunks_count
        }

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Search for similar documents

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of similar documents
        """
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search(query, k=k)

    def reset_collection(self) -> bool:
        """Reset/delete the collection"""
        try:
            client = self._get_client()
            client.delete_collection(self.collection_name)
            self._vectorstore = None
            return True
        except Exception as e:
            print(f"Error resetting collection: {e}")
            return False
