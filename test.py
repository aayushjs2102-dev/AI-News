from services.faiss_services.search_index import FaissSearcher

searcher = FaissSearcher()

results = searcher.search(
    "Artificial Intelligence in healthcare",
    k=5
)

for article in results:

    print()

    print(article["id"])

    print(article["title"])

    print(article["cluster_name"])