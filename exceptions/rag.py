from exceptions.base import AINewsError


class RAGError(AINewsError):
    """Raised when FAISS or RAG processing fails."""
    pass