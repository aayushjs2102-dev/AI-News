"""
Batch classification service.

Classifies all unclassified articles and updates the database.
"""

from services.classification_services.classifier import ZeroShotClassifier
from database.repositories.article_repository import ArticleRepository
from utils.logger import get_logger

logger = get_logger()


def classify_articles(limit: int | None = None):
    """
    Classify all articles where cluster_name IS NULL.
    """

    print("=" * 70)
    print("Starting article classification...")
    print("=" * 70)

    classifier = ZeroShotClassifier()

    articles = ArticleRepository.get_unclassified_articles()

    if limit is not None:
        articles = articles[:limit]

    print(f"\nFound {len(articles)} unclassified articles.\n")

    if len(articles) == 0:
        print("No articles to classify.")
        return

    for index, article in enumerate(articles, start=1):

        print("=" * 70)
        print(f"Processing Article {index}/{len(articles)}")
        print("=" * 70)

        print(f"ID      : {article['id']}")
        print(f"Title   : {article['title']}")
        print(f"Current : {article['cluster_name']}")

        text = f"""
Title:
{article['title']}

Summary:
{article['summary']}
"""

        try:

            print("\nRunning Zero-Shot Classification...")

            result = classifier.classify(text)

            print("Prediction Complete!")

            print(f"Cluster    : {result['cluster']}")
            print(f"Confidence : {result['score']:.4f}")

            print("\nUpdating PostgreSQL...")

            ArticleRepository.update_cluster_name(
                article["id"],
                result["cluster"]
            )

            print("Database Updated Successfully!")

            logger.info(
                f"Article {article['id']} classified as "
                f"{result['cluster']} "
                f"({result['score']:.3f})"
            )

        except Exception as e:

            print("\nERROR OCCURRED")
            print(type(e).__name__)
            print(e)

            logger.exception(
                f"Failed to classify article {article['id']}: {e}"
            )

    print("\n" + "=" * 70)
    print("Classification Finished")
    print("=" * 70)