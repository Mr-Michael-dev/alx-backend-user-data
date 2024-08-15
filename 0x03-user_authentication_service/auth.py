#!/usr/bin/env python3
"""
This module contains auth logic for the API
"""
import bcrypt
from db import DB
from user import User


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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        adds a new user to the database

        Arguments:
        email (str) - user's email
        passowrd (str) - user's password

        Returns:
        user object
        """
        user = self._db._session.query(User).filter_by(email=email).first()

        if user is None:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if a user exits, if exits, check if password matches

        Arguments:
        email (str) - user's email
        passowrd (str) - user's password

        Returns:
        True if user matches, otherwise false
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        saved_password = user.hashed_password.encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), saved_password):
            return True

        return False
