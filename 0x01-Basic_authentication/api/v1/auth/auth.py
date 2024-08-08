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

        for excluded_path in excluded_paths:
            # Handle paths with wildcard '*'
            if excluded_path.endswith('*'):
                if normalized_path.startswith(excluded_path[:-1]):
                    return False
            else:
                # Normalize excluded_path to ensure it ends with a slash
                normalized_excluded_path = excluded_path\
                    if excluded_path.endswith('/') else excluded_path + '/'
                if normalized_path == normalized_excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the authenticated user based on the request
        """
        return None
