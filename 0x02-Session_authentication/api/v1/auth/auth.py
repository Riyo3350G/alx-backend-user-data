#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in
        the list of strings excluded_paths"""
        if not path:
            return True
        if not excluded_paths:
            return True
        path = path.rstrip("/")
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and \
                    path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """method that returns None - request"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """"method that returns None - request"""
        return None

    def session_cookie(self, request=None):
        """method that returns a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'), None)
