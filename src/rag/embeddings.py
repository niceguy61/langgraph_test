"""Embedding model configuration for RAG"""
from langchain_ollama import OllamaEmbeddings
from src.config import settings


def get_embeddings() -> OllamaEmbeddings:
    """Get configured Ollama embeddings model"""
    return OllamaEmbeddings(
        base_url=settings.ollama.host,
        model=settings.ollama.embedding_model
    )
