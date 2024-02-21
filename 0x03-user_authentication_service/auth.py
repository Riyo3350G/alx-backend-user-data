#!/usr/bin/env python3
"""Auth module for the authentication class"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Takes in a password string arguments and returns bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """function that return a uuid string"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method that allows a user to register
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """method that valids user login"""
        try:
            user = self._db.find_user_by(email=email)
            hached_pass = password.encode('utf-8')
            if bcrypt.checkpw(hached_pass, user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """method that create a session id for user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """method thats return user by session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Method that destroy the user session"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Method that reset the passwoed token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """method thats update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password)
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
