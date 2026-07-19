"""
AI Assistant Service

Author: Aayush

Acts as the bridge between the Flask routes and the
RAG system.
"""

from services.rag_services.rag_service import RAGService

from utils.logger import get_logger

logger = get_logger()


class AssistantService:
    """
    Handles AI assistant requests.

    Responsibilities
    ----------------
    - Validate user input
    - Call the RAG service
    - Return a response suitable for the UI
    """

    _instance = None

    _rag = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if self._rag is not None:
            return

        self._rag = RAGService()

    def ask(
        self,
        question: str
    ):
        """
        Ask the AI assistant.

        Parameters
        ----------
        question : str

        Returns
        -------
        dict
        """

        question = question.strip()

        if not question:

            return {
                "success": False,
                "question": "",
                "answer": "Please enter a question.",
                "articles": []
            }

        try:

            logger.info(
                f"Assistant question: {question}"
            )

            result = self._rag.answer(question)

            return {
                "success": True,
                "question": question,
                "answer": result["answer"],
                "articles": result["articles"]
            }

        except Exception as e:

            logger.exception(e)

            return {
                "success": False,
                "question": question,
                "answer": (
                    "Sorry, something went wrong while "
                    "generating the response."
                ),
                "articles": []
            }


assistant_service = AssistantService()