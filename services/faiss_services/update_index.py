"""
Incrementally Update FAISS Index

Author: Aayush
"""

import numpy as np

from database.repositories.article_repository import ArticleRepository

from services.faiss_services.embedding_model import EmbeddingModel

from services.faiss_services.faiss_utils import (
    load_index,
    save_index,
    load_mappings,
    save_mappings
)


def update_faiss_index():

    print("Loading FAISS index...")

    index = load_index()

    vector_to_article, article_to_vector = load_mappings()

    indexed_article_ids = set(article_to_vector.keys())

    new_articles = ArticleRepository.get_unindexed_articles(
        indexed_article_ids
    )

    if not new_articles:

        print("No new articles to index.")

        return

    print(f"Found {len(new_articles)} new articles.")

    model = EmbeddingModel()

    embeddings = []

    next_vector_index = index.ntotal

    for article in new_articles:

        text = f"{article['title']}\n{article['summary']}"

        vector = model.encode(text)

        embeddings.append(vector)

        vector_to_article[next_vector_index] = article["id"]

        article_to_vector[article["id"]] = next_vector_index

        next_vector_index += 1

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    index.add(embeddings)

    save_index(index)

    save_mappings(
        vector_to_article,
        article_to_vector
    )

    print("--------------------------------")

    print("FAISS index updated successfully.")

    print(f"Added vectors : {len(new_articles)}")

    print(f"Total vectors : {index.ntotal}")


if __name__ == "__main__":

    update_faiss_index()