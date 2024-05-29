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

    def create_session(self, email: str) -> str:
        """create session doc"""
        try:
            user = self._db.find_user_by(email=email)
            session_gen = _generate_uuid()
            self._db.update_user(user.id, session_id=session_gen)
            return session_gen
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """get user from session"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None
