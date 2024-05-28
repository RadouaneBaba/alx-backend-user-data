#!/usr/bin/env python3
"""auth module doc"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash a password"""
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError
        except ValueError:
            raise ValueError(f"User {email} already exists")
        except Exception:
            user = self._db.add_user(email, str(_hash_password(password)))
            return user
