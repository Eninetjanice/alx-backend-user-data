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
