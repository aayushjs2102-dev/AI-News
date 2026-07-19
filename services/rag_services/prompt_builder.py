"""
RAG Prompt Builder

Author: Aayush
"""


class PromptBuilder:
    """
    Builds prompts for the AI News Assistant.
    """

    SYSTEM_PROMPT = """
You are an AI News Assistant.

Your job is to answer the user's question using ONLY the news articles provided.

Instructions:

1. Use only the provided news context.
2. Do not invent or assume facts.
3. If the answer is not available in the context, clearly state that.
4. If multiple articles discuss the same topic, combine the information into one coherent answer.
5. Keep responses factual, concise, and well-structured.
6. Do not mention internal systems, databases, retrieval, embeddings, or FAISS.
7. When appropriate, mention the news source naturally within your answer.
""".strip()

    def build(
        self,
        question: str,
        context: str
    ) -> dict:
        """
        Builds the structured prompt components.
        """

        return {
            "system_prompt": self.SYSTEM_PROMPT,
            "context": context,
            "question": question
        }