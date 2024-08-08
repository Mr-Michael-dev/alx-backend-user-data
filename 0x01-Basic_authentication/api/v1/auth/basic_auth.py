#!/usr/bin/env python3
"""
Module contains BasicAuth class taht inherits from Auth
"""
from flask import request
import base64
from typing import List, Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Decode the base64 encoded username and password

        Arguments:
        base64_authorization_header {str} - encoded Base64 string

        Returns:
        decoded value as UTF8 string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_credentials = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_credentials
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """
        Extract the username and password from the decoded Base64 string

        Arguments:
        decoded_base64_authorization_header {str} - decoded Base64 string

        Returns:
        Tuple of username and password
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        username, password = decoded_base64_authorization_header.split(':')

        return (username, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieve a user object from database
        using the provided email and password
        """
        if user_email is None or user_pwd is None:
            return None

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
