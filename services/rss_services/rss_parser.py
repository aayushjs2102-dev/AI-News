"""
RSS Parser

Downloads and parses RSS feeds into a standardized format.
"""

from datetime import datetime

import feedparser

from utils.logger import get_logger

from utils.http_client import HTTPClient

logger = get_logger()


class RSSParser:
    """
    Parses RSS feeds into standardized article dictionaries.
    """

    @staticmethod
    def parse_feed(source: str, feed_url: str) -> list[dict]:
        """
        Parse a single RSS feed.

        Returns:
            list[dict]
        """

        logger.info(f"Fetching RSS feed: {source} -> {feed_url}")

        try:

            response = HTTPClient.get(feed_url)

            if response is None:
                logger.error(f"Unable to download RSS feed: {feed_url}")
                return []

            feed = feedparser.parse(response.content)

            # feedparser sets bozo=True when parsing fails
            if getattr(feed, "bozo", False):
                logger.warning(
                    f"Malformed RSS feed detected: {feed_url}"
                )

            if not feed.entries:
                logger.warning(
                    f"No articles found in feed: {feed_url}"
                )
                return []

            articles = []

            for entry in feed.entries:

                try:

                    if (
                        hasattr(entry, "published_parsed")
                        and entry.published_parsed
                    ):
                        published = datetime(
                            *entry.published_parsed[:6]
                        )
                    else:
                        published = datetime.now()

                    article = {
                        "source": source,
                        "title": getattr(
                            entry,
                            "title",
                            "Untitled"
                        ),
                        "summary": getattr(
                            entry,
                            "summary",
                            ""
                        ),
                        "url": getattr(
                            entry,
                            "link",
                            ""
                        ),
                        "published_at": published
                    }

                    if not article["url"]:
                        logger.warning(
                            "Skipping article with missing URL."
                        )
                        continue

                    articles.append(article)

                except Exception:

                    logger.exception(
                        "Failed to parse an RSS entry."
                    )

            logger.info(
                f"{source}: Parsed {len(articles)} articles."
            )

            return articles

        except Exception:

            logger.exception(
                f"Unable to fetch RSS feed: {feed_url}"
            )

            return []