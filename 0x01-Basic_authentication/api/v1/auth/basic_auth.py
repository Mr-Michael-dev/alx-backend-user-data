#!/usr/bin/env python3
"""
Module contains BasicAuth class taht inherits from Auth
"""
from flask import request
import base64
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Authenticates a user using basic authentication
    """
    def __init__(self) -> None:
        """
        Initialize BasicAuth from Auth
        """
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extract the base64 encoded username and password
        from the authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        parts = authorization_header.split(' ')
        if len(parts) < 2 or parts[0].lower() != 'basic':
            return None

        encoded_credentials = parts[1]

        return encoded_credentials
