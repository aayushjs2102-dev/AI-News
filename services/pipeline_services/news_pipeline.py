"""
News Pipeline

Coordinates the complete news ingestion workflow.
"""

from services.rss_services.rss_collector import RSSCollector

from services.classification_services.classify_articles import (
    classify_articles
)


def run_news_pipeline():
    """
    Complete news ingestion pipeline.
    """

    print("\n" + "=" * 70)
    print("STARTING NEWS PIPELINE")
    print("=" * 70)

    #Step 1
    RSSCollector.collect()

    #Step 2
    classify_articles()

    print("\n" + "=" * 70)
    print("NEWS PIPELINE FINISHED")
    print("=" * 70)