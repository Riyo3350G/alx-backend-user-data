#!/usr/bin/env python3
"""Basic auth module"""
from models.user import User
from api.v1.auth.auth import Auth
from typing import TypeVar, Tuple
import base64


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """method returns the Base64 part of the
        Authorization header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str,
                                           ) -> str:
        """method that returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header)\
                .decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str,
                                 ) -> (str, str):
        """method that returns the user email and password from the
        Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """method that returns the User
        instance based on his email and password"""
        if type(user_email) is not str or user_email is None:
            return None
        if type(user_pwd) is not str or user_pwd is None:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if user is None:
            return None
        if not user:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """method that overloads Auth and
        retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        user, pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user, pwd)
