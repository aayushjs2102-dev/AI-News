"""
PostgreSQL Connection Manager

Provides centralized PostgreSQL connections.
"""

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

from config.config import Config
from utils.logger import get_logger

logger = get_logger()


class DatabaseConnection:
    """
    Handles PostgreSQL database connections.
    """

    @staticmethod
    def get_connection():
        """
        Create and return a PostgreSQL connection.
        """

        try:

            connection = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                cursor_factory=RealDictCursor,
                connect_timeout=10
            )

            logger.info("Connected to PostgreSQL.")

            return connection

        except OperationalError:

            logger.exception("Unable to connect to PostgreSQL.")

            raise