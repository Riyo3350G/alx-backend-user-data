#!/usr/bin/env python3
"""Session DB Authentication Module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """method that creates a session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """method that returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        if not created_at:
            return None
        date_now = datetime.now()
        if (date_now - created_at) > timedelta(seconds=self.session_duration):
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """method that deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        UserSession.load_from_file()
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True
