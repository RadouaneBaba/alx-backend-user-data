#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """hash a password using hashpw"""
    return bcrypt.hashpw(password, bcrypt.gensalt())
