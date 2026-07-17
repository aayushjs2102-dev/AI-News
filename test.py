from services.recommendation_services.recommendation_engine import (
    get_recommendations
)

articles = get_recommendations(1)

print()

for article in articles:

    print(
        article["cluster_name"],
        "|",
        article["title"]
    )