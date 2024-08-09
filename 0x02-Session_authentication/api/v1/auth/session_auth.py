#!/usr/bin/env python3
"""
Module contains SessionAuth class thatt inherits from Auth
"""
from flask import request
import base64
from typing import List, Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Authenticates a user using session authentication
    """
    pass
