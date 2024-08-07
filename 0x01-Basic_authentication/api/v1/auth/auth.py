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
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Normalize the path to ensure it ends with a slash
        normalized_path = path if path.endswith('/') else path + '/'

        # Check if the normalized path is in the excluded_paths
        if normalized_path in excluded_paths:
            return False

        return True

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
