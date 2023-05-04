#!/usr/bin/env python3
"""BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """class BasicAuth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Basic Authentication - Base64 part
        Return:
            Base64 part of the Authorization header
        """
        # Return None if authorization_header is None
        if authorization_header is None:
            return None
        # Return None if authorization_header is not a string
        if not isinstance(authorization_header, str):
            return None
        # Return None if authorization_header doesn’t start by 'Basic '
        if not authorization_header.startswith('Basic '):
            return None
        # Otherwise, return the value after Basic (after the space)
        return authorization_header.split(' ')[1]
