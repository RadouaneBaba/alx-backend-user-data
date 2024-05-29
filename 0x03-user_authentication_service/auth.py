#!/usr/bin/env python3
"""auth module doc"""
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """hash a password"""
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)


def _generate_uuid() -> str:
    """return new str uuid"""
    return str(uuid.uuid4())


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
            user = self._db.add_user(
                email, _hash_password(password).decode("utf-8")
            )
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """valid login method"""
        try:
            user = self._db.find_user_by(email=email)
            hashed_pw = user.hashed_password.encode("utf-8")
            byte_pw = password.encode("utf-8")
            if bcrypt.checkpw(byte_pw, hashed_pw):
                return True
            return False
        except Exception:
            return False
