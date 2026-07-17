from exceptions.base import AINewsError


class ClassificationError(AINewsError):
    """Raised when zero-shot classification fails."""
    pass