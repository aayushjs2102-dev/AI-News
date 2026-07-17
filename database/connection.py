"""
PostgreSQL Connection Manager

Author: Aayush

Provides a centralized PostgreSQL connection for the entire application.
"""

import psycopg2

from psycopg2.extras import RealDictCursor

from config.config import Config


class DatabaseConnection:
    """
    Handles PostgreSQL database connections.
    """

    @staticmethod
    def get_connection():
        """
        Create and return a PostgreSQL connection.
        """

        connection = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            cursor_factory=RealDictCursor
        )

        return connection