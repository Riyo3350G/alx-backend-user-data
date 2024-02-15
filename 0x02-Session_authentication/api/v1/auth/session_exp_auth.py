#!/usr/bin/env python3
"""Session expiration authentication Module"""
from api.v1.auth.session_auth import SessionAuth
import uuid
from models.user import User
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""
    def __init__(self):
        """Constructor"""
        SESSION_DURATION = os.getenv('SESSION_DURATION')
        try:
            session_duration = int(SESSION_DURATION)
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id: str = None) -> str:
        """method that creates a Session ID for a user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """method that returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        user_id = session_dictionary.get("user_id")
        if user_id is None:
            return None
        if self.session_duration <= 0:
            return user_id
        created_at = session_dictionary.get("created_at")
        if created_at is None:
            return None
        date_now = datetime.now()
        if (date_now - created_at) > timedelta(seconds=self.session_duration):
            return None
        return user_id
