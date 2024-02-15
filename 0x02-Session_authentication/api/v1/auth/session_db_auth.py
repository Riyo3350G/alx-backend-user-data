#!/usr/bin/env python3
"""Session DB Authentication Module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
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
        user_session = UserSession.search({"session_id": session_id})
        if user_session is None:
            return None
        if self.session_duration <= 0:
            return user_session.user_id
        if user_session.created_at is None:
            return None
        if (user_session.created_at - self.session_duration) > 0:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """method that deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session is None:
            return False
        user_session.remove()
        return True
