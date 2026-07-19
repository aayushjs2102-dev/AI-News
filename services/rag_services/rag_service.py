"""
RAG Service

Author: Aayush
"""

from services.rag_services.retriever import Retriever
from services.rag_services.context_builder import ContextBuilder
from services.rag_services.prompt_builder import PromptBuilder
from services.rag_services.llm import LLM


class RAGService:
    """
    Coordinates the complete Retrieval-Augmented Generation pipeline.
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        self.retriever = Retriever()
        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()
        self.llm = LLM()

        self._initialized = True

    def answer(
        self,
        question: str,
        top_k: int = 5
    ) -> dict:

        # --------------------------------------------------
        # Retrieve relevant articles
        # --------------------------------------------------

        articles = self.retriever.retrieve(
            question,
            top_k
        )

        # --------------------------------------------------
        # Build context
        # --------------------------------------------------

        context = self.context_builder.build(
            articles
        )

        # --------------------------------------------------
        # Build prompt
        # --------------------------------------------------

        prompt = self.prompt_builder.build(
            question,
            context
        )

        # --------------------------------------------------
        # Generate answer
        # --------------------------------------------------

        answer = self.llm.generate(
            system_prompt=prompt["system_prompt"],
            context=prompt["context"],
            question=prompt["question"]
        )

        # --------------------------------------------------
        # Return response
        # --------------------------------------------------

        return {
            "question": question,
            "answer": answer,
            "articles": articles
        }