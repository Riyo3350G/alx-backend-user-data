#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """method that returns False - path and excluded_paths"""
        return False

    def authorization_header(self, request=None) -> str:
        """method that returns None - request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """"method that returns None - request"""
        return None
