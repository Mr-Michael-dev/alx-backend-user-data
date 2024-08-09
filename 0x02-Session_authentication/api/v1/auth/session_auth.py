#!/usr/bin/env python3
"""
Module contains SessionAuth class thatt inherits from Auth
"""
from flask import request
import base64
from typing import List, Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Authenticates a user using session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a session id using uuid and
        generates a session_id:user_id dict
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = uuid.uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id

        return session_id
