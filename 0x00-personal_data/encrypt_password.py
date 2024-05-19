#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """hash a password using hashpw"""
    byte_pass = bytes(password, "utf-8")
    return bcrypt.hashpw(byte_pass, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """is valid hash password"""
    byte_pass = bytes(password, "utf-8")
    return bcrypt.checkpw(byte_pass, hashed_password)
