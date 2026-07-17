"""
User Preference Repository

Maintains user cluster preference scores.
"""

from database.connection import DatabaseConnection


class PreferenceRepository:

    @staticmethod
    def increment_preference(user_id: int,
                             cluster_name: str,
                             score: float):

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user_cluster_preferences
            (
                user_id,
                cluster_name,
                preference_score
            )
            VALUES (%s, %s, %s)

            ON CONFLICT (user_id, cluster_name)

            DO UPDATE SET

                preference_score =
                    user_cluster_preferences.preference_score
                    + EXCLUDED.preference_score,

                updated_at = CURRENT_TIMESTAMP;
        """, (
            user_id,
            cluster_name,
            score
        ))

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_preferences(user_id: int):

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                cluster_name,
                preference_score

            FROM user_cluster_preferences

            WHERE user_id = %s

            ORDER BY preference_score DESC;
        """, (user_id,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows