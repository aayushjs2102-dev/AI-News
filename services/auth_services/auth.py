"""
Authentication Service

Handles user registration and login.
"""

import bcrypt

from database.repositories.user_repository import UserRepository


# ----------------------------------------------------------
# Register User
# ----------------------------------------------------------

def register_user(username: str, email: str, password: str):
    """
    Register a new user.

    Returns:
        (success: bool, message: str)
    """

    # Username already exists
    if UserRepository.get_user_by_username(username):
        return False, "Username already exists."

    # Email already exists
    if UserRepository.get_user_by_email(email):
        return False, "Email already exists."

    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    UserRepository.create_user(
        username=username,
        email=email,
        password_hash=password_hash
    )

    return True, "Registration successful."


# ----------------------------------------------------------
# Login User
# ----------------------------------------------------------

def login_user(username: str, password: str):
    """
    Authenticate a user.

    Returns:
        (success: bool, user)
    """

    user = UserRepository.get_user_by_username(username)

    if user is None:
        return False, None

    password_matches = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    )

    if not password_matches:
        return False, None

    return True, user