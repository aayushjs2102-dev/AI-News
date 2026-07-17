"""
Application Configuration

Loads all configuration values from the .env file.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY")

    # PostgreSQL
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Google GenAI
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Debug
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"