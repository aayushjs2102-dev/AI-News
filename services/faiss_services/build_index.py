"""
Build FAISS Index

Author: Aayush
"""

import os

import faiss
import numpy as np

from database.repositories.article_repository import ArticleRepository
from services.faiss_services.embedding_model import EmbeddingModel
from services.faiss_services.faiss_utils import (
    save_index,
    save_mappings
)


# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

FAISS_DIR = os.path.join(
    BASE_DIR,
    "faiss"
)


# ----------------------------------------------------------
# Build Index
# ----------------------------------------------------------

def build_faiss_index():

    os.makedirs(
        FAISS_DIR,
        exist_ok=True
    )

    print("Loading articles...")

    articles = ArticleRepository.get_all_articles()

    if not articles:
        print("No articles found.")
        return

    print(f"Found {len(articles)} articles.")

    model = EmbeddingModel()

    embeddings = []

    vector_to_article = {}

    article_to_vector = {}

    for idx, article in enumerate(articles):

        text = f"{article['title']}\n{article['summary']}"

        vector = model.encode(text)

        embeddings.append(vector)

        vector_to_article[idx] = article["id"]

        article_to_vector[article["id"]] = idx

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    print(f"Embedding Dimension: {dimension}")

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    # ----------------------------------------------
    # Save Index & Mappings
    # ----------------------------------------------

    save_index(index)

    save_mappings(
        vector_to_article,
        article_to_vector
    )

    print("--------------------------------")

    print("FAISS index built successfully.")

    print(f"Vectors : {index.ntotal}")

    print("FAISS index saved.")

    print("Mappings saved.")


if __name__ == "__main__":

    build_faiss_index()