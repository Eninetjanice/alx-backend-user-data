#!/usr/bin/env python3
""" Auth """

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hass password method.

    Args:
        password (str): The password string to hash.

    Returns:
        bytes: A salted hash of input password hashed with bcrypt.hashpw.
    """
    random_salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), random_salt)
    return hashed_pwd
