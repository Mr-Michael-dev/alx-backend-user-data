#!/usr/bin/env python3
"""
Module contains Auth class for authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Authenticates a user based on a request
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if the request requires authentication based on
        the provided path and excluded paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the authenticated user based on the request
        """
        return None
