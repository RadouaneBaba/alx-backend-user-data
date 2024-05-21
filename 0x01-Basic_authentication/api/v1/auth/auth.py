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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        new_path = path if path[-1] == "/" else path + "/"
        for e_path in excluded_paths:
            if e_path[-1] == "*":
                if e_path[-2] == "/":
                    return False
                elif new_path.startswith(e_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user implementation"""
        return None
