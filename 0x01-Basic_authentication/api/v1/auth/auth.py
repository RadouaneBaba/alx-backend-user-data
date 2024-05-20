#!/usr/bin/env python3
""" Doc Doc Doc """
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class implementation
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """reuire auth doc"""
        if path is None or excluded_paths in ["", None]:
            return True
        new_path = path if path[-1] == "/" else path + "/"
        if new_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user implementation"""
        return None
