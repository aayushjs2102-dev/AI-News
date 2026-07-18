"""
RSS Collector

Collects news from all configured RSS feeds
and stores new articles in PostgreSQL.
"""

from services.rss_services.rss_feeds import RSS_FEEDS
from services.rss_services.rss_parser import RSSParser

from database.repositories.article_repository import ArticleRepository


class RSSCollector:

    @staticmethod
    def collect():

        total_parsed = 0
        total_inserted = 0
        total_skipped = 0


        print("\n" + "=" * 60)
        print("RSS COLLECTION STARTED")
        print("=" * 60)

        for source, feeds in RSS_FEEDS.items():

            source_parsed = 0
            source_inserted = 0
            source_skipped = 0

            print(f"\nCollecting from {source}...")

            for feed_url in feeds:

                articles = RSSParser.parse_feed(
                    source,
                    feed_url
                )

                for article in articles:

                    source_parsed += 1
                    total_parsed += 1

                    if ArticleRepository.article_exists(
                        article["url"]
                    ):
                        source_skipped += 1
                        total_skipped += 1
                        continue

                    category = "General"

                    url_lower = article["url"].lower()

                    if "technology" in url_lower:
                        category = "Technology"

                    elif "sport" in url_lower:
                        category = "Sports"

                    elif "business" in url_lower:
                        category = "Business"

                    elif "science" in url_lower:
                        category = "Science"

                    ArticleRepository.create_article(
                        source=article["source"],
                        title=article["title"],
                        summary=article["summary"],
                        url=article["url"],
                        published_at=article["published_at"],
                        category=category,
                        cluster_name=None
                    )

                    source_inserted += 1
                    total_inserted += 1

            print(f"Parsed   : {source_parsed}")
            print(f"Inserted : {source_inserted}")
            print(f"Skipped  : {source_skipped}")

        print("\n" + "=" * 60)
        print("RSS COLLECTION SUMMARY")
        print("=" * 60)

        print(f"Total Parsed   : {total_parsed}")
        print(f"Inserted       : {total_inserted}")
        print(f"Skipped        : {total_skipped}")

        print("=" * 60)

