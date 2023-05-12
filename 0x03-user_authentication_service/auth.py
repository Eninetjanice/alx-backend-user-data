#!/usr/bin/env python3
""" Auth """

import uuid
from bcrypt import checkpw, hashpw, gensalt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hass password method.

    Args:
        password (str): The password string to hash.

    Returns:
        bytes: A salted hash of input password hashed with bcrypt.hashpw.
    """
    random_salt = gensalt()
    hashed_pwd = hashpw(password.encode('utf-8'), random_salt)
    return hashed_pwd


def _generate_uuid() -> str:
    """
    Generates UUIDs.
    Return:
    String representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register new user with given email and password.

        Args:
            email (str): Email of the new user.
            password (str): Password of the new user.

        Returns:
            User: The newly registered User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        # If user exist with passed email, raise a ValueError
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Credentials validation
        Args:
            email (str): User's email
            password (str): User's password
        Return:
            True: if user's email matches with pwd. Use bcrypt.checkpw.
            False: in any other case
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                if checkpw(password.encode('utf-8'), user.hashed_password):
                    return True
        except NoResultFound and Exception:
            pass
        return False

    def create_session(self, email: str) -> str:
        """
        Get session_id by finding user corresponding to an email,
        generating a new UUID and storing it in the db as session_id.
        Args:
            email (str): User's email.
        Return:
            session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                return session_id
        except NoResultFound:
            pass
