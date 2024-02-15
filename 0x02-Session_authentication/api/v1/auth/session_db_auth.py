#!/usr/bin/env python3
"""Session DB Authentication Module"""
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """method that creates a session ID"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = self.user_id_by_session_id.get(session_id)
        if user_session is None:
            return None
        user_session.user_id = user_id
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """"method that returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        user_session = self.user_id_by_session_id.get(session_id)
        if user_session is None:
            return None
        if self.session_duration <= 0:
            return user_session.user_id
        if user_session.created_at is None:
            return None
        from datetime import datetime, timedelta
        date_now = datetime.now()
        created_at = user_session.created_at
        if (date_now - created_at) > timedelta(seconds=self.session_duration):
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """"method that deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = self.user_id_by_session_id.get(session_id)
        if user_session is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
