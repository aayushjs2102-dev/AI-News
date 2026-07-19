"""
Analytics Repository

Author: Aayush

Provides analytics data from PostgreSQL.
"""

from database.connection import DatabaseConnection


class AnalyticsRepository:
    """
    Repository for analytics queries.
    """

    # ----------------------------------------------------------
    # Total Users
    # ----------------------------------------------------------

    @staticmethod
    def get_total_users() -> int:

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) AS count
            FROM users;
        """)

        total = cur.fetchone()["count"]

        cur.close()
        conn.close()

        return total

    # ----------------------------------------------------------
    # Total Articles
    # ----------------------------------------------------------

    @staticmethod
    def get_total_articles() -> int:

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) AS count
            FROM articles;
        """)

        total = cur.fetchone()["count"]

        cur.close()
        conn.close()

        return total

    # ----------------------------------------------------------
    # Articles Collected Today
    # ----------------------------------------------------------

    @staticmethod
    def get_articles_today() -> int:

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) AS count
            FROM articles
            WHERE DATE(collected_at) = CURRENT_DATE;
        """)

        total = cur.fetchone()["count"]

        cur.close()
        conn.close()

        return total

    # ----------------------------------------------------------
    # Total Likes
    # ----------------------------------------------------------

    @staticmethod
    def get_total_likes() -> int:

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) AS count
            FROM user_interactions
            WHERE interaction_type = 'like';
        """)

        total = cur.fetchone()["count"]

        cur.close()
        conn.close()

        return total

    # ----------------------------------------------------------
    # Total Bookmarks
    # ----------------------------------------------------------

    @staticmethod
    def get_total_bookmarks() -> int:

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) AS count
            FROM user_interactions
            WHERE interaction_type = 'bookmark';
        """)

        total = cur.fetchone()["count"]

        cur.close()
        conn.close()

        return total

    # ----------------------------------------------------------
    # Top Clusters
    # ----------------------------------------------------------

    @staticmethod
    def get_top_clusters(limit: int = 10):

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                cluster_name,
                COUNT(*) AS total
            FROM articles
            WHERE cluster_name IS NOT NULL
            GROUP BY cluster_name
            ORDER BY total DESC
            LIMIT %s;
            """,
            (limit,)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {
                "cluster_name": row["cluster_name"],
                "count": row["total"]
            }
            for row in rows
        ]

    # ----------------------------------------------------------
    # Top News Sources
    # ----------------------------------------------------------

    @staticmethod
    def get_top_sources(limit: int = 10):

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                source,
                COUNT(*) AS total
            FROM articles
            GROUP BY source
            ORDER BY total DESC
            LIMIT %s;
            """,
            (limit,)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {
                "source": row["source"],
                "count": row["total"]
            }
            for row in rows
        ]

    # ----------------------------------------------------------
    # Recent User Interactions
    # ----------------------------------------------------------

    @staticmethod
    def get_recent_interactions(limit: int = 20):

        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                u.username,
                a.title,
                ui.interaction_type,
                ui.interaction_time
            FROM user_interactions ui
            JOIN users u
                ON ui.user_id = u.id
            JOIN articles a
                ON ui.article_id = a.id
            ORDER BY ui.interaction_time DESC
            LIMIT %s;
            """,
            (limit,)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {
                "username": row["username"],
                "title": row["title"],
                "interaction_type": row["interaction_type"],
                "interaction_time": row["interaction_time"]
            }
            for row in rows
        ]


analytics_repository = AnalyticsRepository()