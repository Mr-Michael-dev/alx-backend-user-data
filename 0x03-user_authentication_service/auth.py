#!/usr/bin/env python3
"""
This module contains auth logic for the API
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Generates a salted hash of the input password, hashed with bcrypt.hashpw

    Arguments:
    password (str) - password to be hashed

    Returns:
    hashed password in bytes
    """
    salt = bcrypt.gensalt(10)
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_pwd
