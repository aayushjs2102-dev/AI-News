"""
Article Repository

Handles all database operations for the articles table.
"""

from database.connection import DatabaseConnection


class ArticleRepository:

    @staticmethod
    def create_article(
        source: str,
        title: str,
        summary: str,
        url: str,
        published_at,
        category: str,
        cluster_id: str = None
    ):
        """
        Insert a new article.
        """

        query = """
        INSERT INTO articles
        (
            source,
            title,
            summary,
            url,
            published_at,
            category,
            cluster_id
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING id;
        """

        connection = DatabaseConnection.get_connection()

        try:
            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        source,
                        title,
                        summary,
                        url,
                        published_at,
                        category,
                        cluster_id
                    )
                )

                article_id = cursor.fetchone()["id"]

            connection.commit()

            return article_id

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def get_article_by_url(url: str):

        query = """
        SELECT *
        FROM articles
        WHERE url=%s;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query, (url,))

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_article_by_id(article_id: int):

        query = """
        SELECT *
        FROM articles
        WHERE id=%s;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query, (article_id,))

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def get_latest_articles(limit: int = 20):

        query = """
        SELECT *
        FROM articles
        ORDER BY published_at DESC
        LIMIT %s;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query, (limit,))

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_articles_by_cluster(cluster_id: str):

        query = """
        SELECT *
        FROM articles
        WHERE cluster_id=%s
        ORDER BY published_at DESC;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query, (cluster_id,))

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def get_articles_by_category(category: str):

        query = """
        SELECT *
        FROM articles
        WHERE category=%s
        ORDER BY published_at DESC;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query, (category,))

                return cursor.fetchall()

        finally:
            connection.close()