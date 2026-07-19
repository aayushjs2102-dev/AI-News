"""
Application Configuration

Loads all configuration values from the .env file.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # ==========================================================
    # Flask
    # ==========================================================

    SECRET_KEY = os.getenv("SECRET_KEY")

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    # ==========================================================
    # PostgreSQL
    # ==========================================================

    DB_HOST = os.getenv("DB_HOST")

    DB_PORT = int(
        os.getenv(
            "DB_PORT",
            5432
        )
    )

    DB_NAME = os.getenv("DB_NAME")

    DB_USER = os.getenv("DB_USER")

    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # ==========================================================
    # Zero-shot Classification
    # ==========================================================

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "facebook/bart-large-mnli"
    )

    # ==========================================================
    # OpenRouter
    # ==========================================================

    OPENROUTER_API_KEY = os.getenv(
        "OPENROUTER_API_KEY"
    )

    OPENROUTER_MODEL = os.getenv(
        "OPENROUTER_MODEL",
        "deepseek/deepseek-chat-v3-0324:free"
    )

    # ==========================================================
    # RAG Configuration
    # ==========================================================

    # Number of articles returned to the LLM.
    RAG_TOP_K = int(
        os.getenv(
            "RAG_TOP_K",
            5
        )
    )

    # Number of candidates initially retrieved from FAISS.
    # A larger value improves reranking quality.
    RAG_INITIAL_SEARCH_K = int(
        os.getenv(
            "RAG_INITIAL_SEARCH_K",
            25
        )
    )

    # Minimum FAISS similarity score required for an article
    # to be considered relevant.
    RAG_MIN_SIMILARITY = float(
        os.getenv(
            "RAG_MIN_SIMILARITY",
            0.65
        )
    )

    # Minimum confidence required before the predicted
    # cluster is used as a reranking signal.
    RAG_CLASSIFICATION_THRESHOLD = float(
        os.getenv(
            "RAG_CLASSIFICATION_THRESHOLD",
            0.40
        )
    )

    # ==========================================================
    # LLM Generation
    # ==========================================================

    RAG_TEMPERATURE = float(
        os.getenv(
            "RAG_TEMPERATURE",
            0.2
        )
    )

    RAG_MAX_TOKENS = int(
        os.getenv(
            "RAG_MAX_TOKENS",
            600
        )
    )