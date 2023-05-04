#!/usr/bin/env python3
"""
Session Auth class that inherits from Auth
"""
from api.v1.auth.auth import Auth
from typing import Dict
import os
import uuid


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


if os.getenv('AUTH_TYPE') == 'session':
    auth = SessionAuth()
else:
    auth = Auth()
