"""
Build FAISS Index

Author: Aayush
"""

import os
import pickle

import faiss
import numpy as np

from database.repositories.article_repository import ArticleRepository
from services.faiss_services.embedding_model import EmbeddingModel


# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

FAISS_DIR = os.path.join(BASE_DIR, "faiss")

INDEX_PATH = os.path.join(
    FAISS_DIR,
    "article_index.faiss"
)

MAPPING_PATH = os.path.join(
    FAISS_DIR,
    "article_mapping.pkl"
)


# ----------------------------------------------------------
# Build Index
# ----------------------------------------------------------

def build_faiss_index():

    os.makedirs(FAISS_DIR, exist_ok=True)

    print("Loading articles...")

    articles = ArticleRepository.get_all_articles()

    if not articles:
        print("No articles found.")
        return

    print(f"Found {len(articles)} articles.")

    model = EmbeddingModel()

    embeddings = []

    mapping = {}

    for idx, article in enumerate(articles):

        text = f"{article['title']}\n{article['summary']}"

        vector = model.encode(text)

        embeddings.append(vector)

        mapping[idx] = article["id"]

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    print(f"Embedding Dimension: {dimension}")

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(
        MAPPING_PATH,
        "wb"
    ) as file:

        pickle.dump(
            mapping,
            file
        )

    print("--------------------------------")

    print("FAISS index built successfully.")

    print(f"Vectors : {index.ntotal}")

    print(f"Saved   : {INDEX_PATH}")

    print(f"Mapping : {MAPPING_PATH}")


if __name__ == "__main__":

    build_faiss_index()