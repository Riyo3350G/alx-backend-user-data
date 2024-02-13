#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in
        the list of strings excluded_paths"""
        if path is None:
            return True
        if path[len(path) - 1] != '/':
            path += '/'
        astericks = [stars[:-1]
                     for stars in excluded_paths if stars[-1] == '*']
        for star in astericks:
            if path.startswith(star):
                return False
        if excluded_paths is None or not excluded_paths:
            return True
        if path not in excluded_paths:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """method that returns None - request"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """"method that returns None - request"""
        return None
