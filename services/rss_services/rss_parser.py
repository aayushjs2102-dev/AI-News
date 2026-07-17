"""
RSS Parser

Downloads and parses RSS feeds into a standardized format.
"""

from datetime import datetime
import feedparser


class RSSParser:

    @staticmethod
    def parse_feed(source: str, feed_url: str):
        """
        Parse a single RSS feed.

        Returns:
            List[dict]
        """

        feed = feedparser.parse(feed_url)

        articles = []

        for entry in feed.entries:

            published = None

            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(
                    *entry.published_parsed[:6]
                )
            else:
                published = datetime.now()

            article = {
                "source": source,
                "title": getattr(entry, "title", ""),
                "summary": getattr(entry, "summary", ""),
                "url": getattr(entry, "link", ""),
                "published_at": published
            }

            articles.append(article)

        return articles