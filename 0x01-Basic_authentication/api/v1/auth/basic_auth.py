#!/usr/bin/env python3
"""BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


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

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Basic Authentication - Base64 decode
        Return:
            Decode value of Base64 str base64_authorization_header
        """
        # Return None if base64_authorization_header is None
        if base64_authorization_header is None:
            return None
        # Return None if base64_authorization_header is not a string
        if not isinstance(base64_authorization_header, str):
            return None
        # Return None if base64_authorization_header is not a valid Base64
        # Otherwise, return decoded value as UTF8 string - use decode('utf-8')
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Basic Authentication - User credentials extraction
        Returns:
            2 values:
            user email and password from the Base64 decoded value
        """
        # Return None, None if decoded_base64_authorization_header is None
        if decoded_base64_authorization_header is None:
            return None, None
        # Return None, None if decoded_base64_authorization_header is not str
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        # Return None, None if decoded_base64_authorization_header lacks :
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # Else, return user email & user password - the 2 values separated by :
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
        Basic Authentication - User credentials extraction
        Returns:
            User instance based on his email and password.
        """
        # Return None if user_email is None or not a string
        if user_email is None or not isinstance(user_email, str):
            return None
        # Return None if user_pwd is None or not a string
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        # Return None if db lacks User instance with email == user_email
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        # Return None if user_pwd =! pwd of the User instance found
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        # Otherwise, return the User instance
        return user
