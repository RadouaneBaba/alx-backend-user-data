#!/usr/bin/env python3
"""Doc Doc DOc"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic auth implementation"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extract base64 authorization header"""
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode base64 authorization header"""
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode(
                "utf-8"
            )
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract user credentials from base64 authorization header"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or not ":" in decoded_base64_authorization_header
        ):
            return None, None
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """ "user based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search({"email": user_email})

        if not user_list:
            return None

        user = user_list[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar("User"):
        """Return the current user"""
        header = self.authorization_header(request)
        base_64auth = self.extract_base64_authorization_header(header)
        decode_header = self.decode_base64_authorization_header(base_64auth)
        user_info = self.extract_user_credentials(decode_header)
        return self.user_object_from_credentials(*user_info)
