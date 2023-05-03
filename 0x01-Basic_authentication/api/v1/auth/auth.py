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
            True - if the path is not in the list of strings excluded_paths
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        # Add trailing slash to path if not present
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            # Add trailing slash to excluded_path if not present
            if not excluded_path.endswith('/'):
                excluded_path += '/'
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Request validation
        Returns authorization header
        Return:
            None - If request is None or
            request doesn’t contain the header key Authorization
            Otherwise, return the value of the header request Authorization
        """
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            None (request will be the Flask request object)
        """
        return None
