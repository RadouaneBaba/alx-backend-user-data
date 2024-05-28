#!/usr/bin/env python3
"""auth module doc"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash a password"""
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)
