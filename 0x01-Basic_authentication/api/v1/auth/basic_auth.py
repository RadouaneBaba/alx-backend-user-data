#!/usr/bin/env python3
"""Doc Doc DOc"""
from api.v1.auth.auth import Auth
import base64


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
        if authorization_header.startswith("Basic "):
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
