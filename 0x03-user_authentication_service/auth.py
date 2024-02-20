#!/usr/bin/env python3
"""Auth module for the authentication class"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Takes in a password string arguments and returns bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
