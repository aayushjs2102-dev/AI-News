from exceptions.base import AINewsError


class HTTPRequestError(AINewsError):
    """Raised when an HTTP request fails."""
    pass