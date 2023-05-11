#!/usr/bin/env python3
""" Auth """

from bcrypt import hashpw, gensalt
from db import DB
# from sqlalchemy.orm.exc import NoResultFound
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
        from sqlalchemy.orm.exc import NoResultFound
        try:
            self._db.find_user_by(email=email)
        except ValueError:
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user
