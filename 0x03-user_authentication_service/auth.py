#!/usr/bin/env python3
"""
This module contains auth logic for the API
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid
from typing import Optional


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

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        find the user corresponding to the session id

        Arguments:
        session_id (str) - session id

        Returns:
        user object if session exists, otherwise None
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroy the session for the user

        Arguments:
        user_id (int) - id of user
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        find the user corresponding to the email,
        generate a new UUID and store it in the database as the reset_token

        Arguments:
        email (str) - user's email

        Returns:
        reset_token (str) - newly generated reset token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        find the user corresponding to the reset_token,
        update the password in the database

        Arguments:
        reset_token (str) - reset token
        password (str) - new password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_pwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_pwd)
        self._db.update_user(user.id, reset_token=None)

        return None
