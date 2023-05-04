#!/usr/bin/env python3
"""
Session Auth class that inherits from Auth
"""
from api.v1.auth.auth import Auth
import os


class SessionAuth(Auth):
    """
    Session Authentication Class
    """
    pass


if os.getenv('AUTH_TYPE') == 'session':
    auth = SessionAuth()
else:
    auth = Auth()
