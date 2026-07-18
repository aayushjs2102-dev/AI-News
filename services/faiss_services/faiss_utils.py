"""
FAISS Utility Functions

Author: Aayush
"""

import os
import pickle

import faiss

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

FAISS_DIR = os.path.join(
    BASE_DIR,
    "faiss"
)

INDEX_PATH = os.path.join(
    FAISS_DIR,
    "article_index.faiss"
)

VECTOR_MAPPING_PATH = os.path.join(
    FAISS_DIR,
    "vector_to_article.pkl"
)

REVERSE_MAPPING_PATH = os.path.join(
    FAISS_DIR,
    "article_to_vector.pkl"
)


def load_index():

    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(
            f"FAISS index not found: {INDEX_PATH}"
        )

    return faiss.read_index(INDEX_PATH)


def save_index(index):

    os.makedirs(
        FAISS_DIR,
        exist_ok=True
    )

    faiss.write_index(
        index,
        INDEX_PATH
    )


def load_mappings():

    with open(
        VECTOR_MAPPING_PATH,
        "rb"
    ) as file:

        vector_to_article = pickle.load(file)

    with open(
        REVERSE_MAPPING_PATH,
        "rb"
    ) as file:

        article_to_vector = pickle.load(file)

    return (
        vector_to_article,
        article_to_vector
    )


def save_mappings(
    vector_to_article,
    article_to_vector
):

    with open(
        VECTOR_MAPPING_PATH,
        "wb"
    ) as file:

        pickle.dump(
            vector_to_article,
            file
        )

    with open(
        REVERSE_MAPPING_PATH,
        "wb"
    ) as file:

        pickle.dump(
            article_to_vector,
            file
        )


