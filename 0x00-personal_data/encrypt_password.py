#!/usr/bin/env python3
"""
Password encryption
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns salted, hashed password, which is a dtring byte, using bcrypt.
    """
    # Generate random salt
    salt = bcrypt.gensalt()
    # Hash password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Password validator, using bcrypt.
    Arguments:
        hashed_password: bytes type
        password: string type
    Return value: boolean
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
