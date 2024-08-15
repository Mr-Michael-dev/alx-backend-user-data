#!/usr/bin/env python3
"""
This module contains auth logic for the API
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid


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


def _generate_uuid() -> str:
    """
    Generates and returns a string representation of a new UUID
    """
    uid = str(uuid.uuid4())
    return uid


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
        password (str) - user's password

        Returns:
        user object
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if a user exits, if exits, check if password matches

        Arguments:
        email (str) - user's email
        password (str) - user's password

        Returns:
        True if user matches, otherwise false
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        saved_password = user.hashed_password
        if bcrypt.checkpw(password.encode('utf-8'), saved_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email,
        generate a new UUID and store it in the database

        Arguments:
        email (str) - user's email

        Returns:
        session_id (str) - newly generated session id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id
