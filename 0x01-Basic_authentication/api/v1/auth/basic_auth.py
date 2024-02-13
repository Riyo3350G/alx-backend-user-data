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
        # Return None if user_email or user_pwd is not provided or not a string
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        # Use the search class method of User
        # to lookup the list of users based on their email
        users = User.search({'email': user_email})

        # Return None if no user found in the database
        if not users:
            return None

        # Check if user_pwd is the password of the User instance found
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        # Return None if user_pwd is not the password of any User instance
        return None
