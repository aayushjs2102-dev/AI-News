from exceptions.base import AINewsError


class RSSParseError(AINewsError):
    """Raised when an RSS feed cannot be parsed."""
    pass