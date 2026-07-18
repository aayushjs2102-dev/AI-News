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
        cluster_name: str = None
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
            cluster_name
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
                        cluster_name
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
    def get_articles_by_cluster(cluster_name: str):

        query = """
        SELECT *
        FROM articles
        WHERE cluster_name=%s
        ORDER BY published_at DESC;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query, (cluster_name,))

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


    @staticmethod
    def article_exists(url: str) -> bool:
        """
        Check whether an article with the given URL already exists.
        """

        query = """
        SELECT EXISTS(
            SELECT 1
            FROM articles
            WHERE url = %s
        ) AS exists;
        """

        connection = DatabaseConnection.get_connection()

        try:
            with connection.cursor() as cursor:

                cursor.execute(query, (url,))

                return cursor.fetchone()["exists"]

        finally:
            connection.close()

    @staticmethod
    def get_unclassified_articles():

        query = """
        SELECT *
        FROM articles
        WHERE cluster_name IS NULL
        ORDER BY collected_at ASC;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(query)

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def update_cluster_name(
        article_id: int,
        cluster_name: str
    ):

        query = """
        UPDATE articles
        SET cluster_name = %s
        WHERE id = %s;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        cluster_name,
                        article_id
                    )
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    

    @staticmethod
    def get_cluster_name(article_id: int):
        """
        Returns the cluster name for an article.

        Parameters
        ----------
        article_id : int
            ID of the article.

        Returns
        -------
        str | None
            Cluster name if found, otherwise None.
        """

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cluster_name
            FROM articles
            WHERE id = %s;
        """, (article_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            return None

        return row["cluster_name"]
    

    @staticmethod
    def get_articles_by_clusters(cluster_names, limit=20):
        """
        Returns the newest articles belonging to the given clusters.
        """

        if not cluster_names:
            return []

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        placeholders = ",".join(["%s"] * len(cluster_names))

        query = f"""
            SELECT *
            FROM articles
            WHERE cluster_name IN ({placeholders})
            ORDER BY published_at DESC
            LIMIT %s;
        """

        cursor.execute(
            query,
            (*cluster_names, limit)
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    

    @staticmethod
    def get_trending_articles(limit: int = 20):
        """
        Returns trending articles ranked by interaction score.
        """

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT

                a.*,

                COALESCE(
                    SUM(
                        CASE ui.interaction_type
                            WHEN 'view' THEN 1
                            WHEN 'like' THEN 3
                            WHEN 'bookmark' THEN 5
                            ELSE 0
                        END
                    ),
                    0
                ) AS trending_score

            FROM articles a

            LEFT JOIN user_interactions ui
                ON a.id = ui.article_id

            GROUP BY a.id

            ORDER BY
                trending_score DESC,
                a.published_at DESC

            LIMIT %s;
        """, (limit,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    

    @staticmethod
    def get_candidate_articles(cluster_names: list[str], limit: int = 50):
        """
        Returns candidate articles from the given clusters.

        Parameters
        ----------
        cluster_names : list[str]
            Preferred cluster names.

        limit : int
            Maximum number of articles to return.

        Returns
        -------
        list[dict]
        """

        if not cluster_names:
            return []

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        placeholders = ",".join(["%s"] * len(cluster_names))

        query = f"""
            SELECT *
            FROM articles
            WHERE cluster_name IN ({placeholders})
            ORDER BY published_at DESC
            LIMIT %s;
        """

        cursor.execute(
            query,
            (*cluster_names, limit)
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    

    @staticmethod
    def search_articles(query: str, limit: int = 20):
        """
        Search articles by title and summary.

        Parameters
        ----------
        query : str
            Search keyword entered by the user.

        limit : int
            Maximum number of results.

        Returns
        -------
        list[dict]
            Matching articles.
        """

        sql = """
        SELECT *
        FROM articles
        WHERE
            title ILIKE %s
            OR
            summary ILIKE %s
        ORDER BY
            published_at DESC
        LIMIT %s;
        """

        connection = DatabaseConnection.get_connection()

        try:

            with connection.cursor() as cursor:

                search_term = f"%{query}%"

                cursor.execute(
                    sql,
                    (
                        search_term,
                        search_term,
                        limit
                    )
                )

                return cursor.fetchall()

        finally:
            connection.close()