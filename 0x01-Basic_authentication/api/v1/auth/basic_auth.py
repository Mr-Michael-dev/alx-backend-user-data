#!/usr/bin/env python3
"""
Module contains BasicAuth class taht inherits from Auth
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Authenticates a user using basic authentication
    """
    pass
