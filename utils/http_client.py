"""
HTTP Client

Provides centralized HTTP requests with retries,
timeouts, and logging.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.logger import get_logger

logger = get_logger()


class HTTPClient:

    _session = None

    @classmethod
    def get_session(cls):
        """
        Create a singleton requests session.
        """

        if cls._session is None:

            session = requests.Session()

            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[
                    429,
                    500,
                    502,
                    503,
                    504
                ],
                allowed_methods=["GET"]
            )

            adapter = HTTPAdapter(
                max_retries=retry_strategy
            )

            session.mount("http://", adapter)
            session.mount("https://", adapter)

            session.headers.update({
                "User-Agent":
                "AI-News-Recommendation-System/1.0"
            })

            cls._session = session

        return cls._session

    @classmethod
    def get(cls, url: str):

        try:

            logger.info(f"Downloading: {url}")

            response = cls.get_session().get(
                url,
                timeout=(5, 15)
            )

            response.raise_for_status()

            logger.info(
                f"Downloaded successfully: {url}"
            )

            return response

        except requests.RequestException:

            logger.exception(
                f"Failed downloading: {url}"
            )

            return None