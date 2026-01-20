"""RAG Retriever for document search"""
from typing import List, Optional
from langchain_core.documents import Document

from .vectorstore import VectorStoreManager


class RAGRetriever:
    """Retriever for RAG-based document search"""

    def __init__(self, vectorstore_manager: Optional[VectorStoreManager] = None):
        self.vectorstore_manager = vectorstore_manager or VectorStoreManager()

    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """
        Retrieve relevant documents for a query

        Args:
            query: Search query
            k: Number of documents to retrieve

        Returns:
            List of relevant documents
        """
        return self.vectorstore_manager.similarity_search(query, k=k)

    def retrieve_with_context(self, query: str, k: int = 4) -> str:
        """
        Retrieve documents and format as context string

        Args:
            query: Search query
            k: Number of documents to retrieve

        Returns:
            Formatted context string
        """
        documents = self.retrieve(query, k=k)

        if not documents:
            return "관련 문서를 찾을 수 없습니다."

        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("filename", "Unknown")
            week = doc.metadata.get("week", "")
            day = doc.metadata.get("day", "")

            location = f"{week}/{day}" if week and day else source

            context_parts.append(
                f"[문서 {i}] ({location})\n{doc.page_content[:500]}..."
                if len(doc.page_content) > 500
                else f"[문서 {i}] ({location})\n{doc.page_content}"
            )

        return "\n\n---\n\n".join(context_parts)

    def get_week_documents(self, week: int) -> List[Document]:
        """
        Get all documents for a specific week

        Args:
            week: Week number (1-4)

        Returns:
            List of documents for that week
        """
        # Search with week-specific query
        query = f"week{week} 학습 내용"
        docs = self.retrieve(query, k=10)

        # Filter by week metadata
        return [
            doc for doc in docs
            if doc.metadata.get("week", "").lower() == f"week{week}"
        ]
