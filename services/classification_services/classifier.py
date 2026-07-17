"""
Zero-shot classification service.

Loads the model lazily and reuses it for all future
classification requests.
"""

from threading import Lock

from transformers import pipeline

from config.config import Config
from services.classification_services.labels import CLUSTERS
from utils.logger import get_logger

logger = get_logger()


class ZeroShotClassifier:
    """
    Thread-safe singleton zero-shot classifier.
    """

    _instance = None
    _pipeline = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @classmethod
    def _load_pipeline(cls):

        if cls._pipeline is not None:
            return

        with cls._lock:

            if cls._pipeline is None:

                logger.info(f"Loading model: {Config.MODEL_NAME}")

                cls._pipeline = pipeline(
                    task="zero-shot-classification",
                    model=Config.MODEL_NAME
                )

                logger.info("Zero-shot classifier ready.")

    def classify(self, text: str):

        self._load_pipeline()

        result = self._pipeline(
            text,
            candidate_labels=CLUSTERS,
            multi_label=False
        )

        return {
            "cluster": result["labels"][0],
            "score": float(result["scores"][0]),
            "labels": result["labels"],
            "scores": [float(s) for s in result["scores"]]
        }