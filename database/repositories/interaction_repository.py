"""
Interaction Repository

Handles database operations for user interactions.
"""

from database.connection import DatabaseConnection


class InteractionRepository:

    @staticmethod
    def log_interaction(
        user_id: int,
        article_id: int,
        interaction_type: str
    ):
        """
        Save a user interaction.
        """

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user_interactions
            (
                user_id,
                article_id,
                interaction_type
            )
            VALUES (%s, %s, %s);
        """, (
            user_id,
            article_id,
            interaction_type
        ))

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_user_interactions(user_id: int):
        """
        Returns all interactions of a user.
        """

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM user_interactions
            WHERE user_id = %s
            ORDER BY interaction_time DESC;
        """, (user_id,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows