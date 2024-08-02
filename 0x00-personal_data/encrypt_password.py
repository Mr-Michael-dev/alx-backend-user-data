#!/usr/bin/env python3
"""
Contains a function called hash_password that hashes a password using bcrypt.
"""
import bcrypt


def hash_password(password) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
