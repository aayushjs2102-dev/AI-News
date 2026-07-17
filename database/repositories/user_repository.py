"""
User Repository

Handles all database operations for the users table.
"""
from utils.logger import get_logger

logger = get_logger()

from database.connection import DatabaseConnection


class UserRepository:

    @staticmethod
    def create_user(username: str, email: str, password_hash: str):
        """
        Insert a new user into the database.
        """

        query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        username,
                        email,
                        password_hash
                    )
                )

                user_id = cursor.fetchone()["id"]

            connection.commit()

            logger.info(
                f"User '{username}' registered successfully."
            )

            return user_id

        except Exception:

            connection.rollback()

            logger.exception(
                f"Failed to register user '{username}'."
            )

            raise

        finally:

            connection.close()

    @staticmethod
    def get_user_by_username(username: str):

        query = """
        SELECT *
        FROM users
        WHERE username = %s;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query, (username,))

                user = cursor.fetchone()

                if user:
                    logger.info(
                        f"User '{username}' found."
                    )
                else:
                    logger.warning(
                        f"User '{username}' not found."
                    )

                return user

        finally:

            connection.close()

    @staticmethod
    def get_user_by_email(email: str):

        query = """
        SELECT *
        FROM users
        WHERE email = %s;
        """

        connection = DatabaseConnection.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_user_by_id(user_id: int):

        query = """
        SELECT *
        FROM users
        WHERE id = %s;
        """

        connection = DatabaseConnection.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()

        finally:
            connection.close()