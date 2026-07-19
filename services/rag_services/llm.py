"""
OpenRouter LLM

Author: Aayush
"""

import requests

from config.config import Config


class LLM:
    """
    OpenRouter client for the AI News Assistant.
    """

    _instance = None

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        self.api_key = Config.OPENROUTER_API_KEY
        self.model = Config.OPENROUTER_MODEL

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in .env"
            )

        self._initialized = True

    def generate(
        self,
        system_prompt: str,
        context: str,
        question: str,
        temperature: float = 0.2,
        max_tokens: int = 600
    ) -> str:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        user_message = f"""
NEWS CONTEXT

{context}

--------------------------------------------------

USER QUESTION

{question}
"""

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if not response.ok:
            raise RuntimeError(
                f"""
OpenRouter Error

Status Code: {response.status_code}

Response:
{response.text}
"""
            )

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()