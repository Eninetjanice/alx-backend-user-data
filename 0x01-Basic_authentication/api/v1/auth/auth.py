#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth():
    """
    Authentication Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required
        Return:
            False (path and excluded_paths)
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns authorization header
        Return:
            None (request will be the Flask request object)
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            None (request will be the Flask request object)
        """
        return None
