#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar
from os import getenv


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
            # Improve excluded_path
            if '*' in excluded_path:
                prefix = excluded_path.split('*')[0]
                if path.startswith(prefix):
                    return False
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
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            None (request will be the Flask request object)
        """
        return None

    def session_cookie(self, request=None):
        """ Session Cookie.
        Return:
            a cookie value from a request based on a condition
        """
        # Return None if request is None
        if request is None:
            return None
        # Return cookie val named _my_session_id from request
        _my_session_id = getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
