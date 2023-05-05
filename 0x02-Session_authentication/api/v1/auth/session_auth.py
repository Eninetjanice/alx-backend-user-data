#!/usr/bin/env python3
"""
Session Auth class that inherits from Auth
"""
from api.v1.auth.auth import Auth
from typing import Dict
import os
import uuid

from models.user import User


class SessionAuth(Auth):
    """
    Session Authentication Class
    """
    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generate Session ID for user_id
        Return:
            None or Session ID based on a condition
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        User ID for Session ID
        Return:
            User ID based on a Session ID
        """
        # Return None if session_id is None
        if session_id is None:
            return None
        # Return None if session_id is not a string
        if not isinstance(session_id, str):
            return None
        # Return value (User ID) for the key session_id in the dict
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None): 
        """
        (overload)
        Return:
            User instance based on a cookie value
        """
        _my_session_id = self.session_cookie(request)
        session_user_id = self.user_id_for_session_id(_my_session_id)
        user_id = User.get(session_user_id)
        return user_id


if os.getenv('AUTH_TYPE') == 'session':
    auth = SessionAuth()
else:
    auth = Auth()
