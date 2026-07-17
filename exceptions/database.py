from exceptions.base import AINewsError


class DatabaseConnectionError(AINewsError):
    """Raised when a database connection cannot be established."""
    pass


class DatabaseQueryError(AINewsError):
    """Raised when a database query fails."""
    pass