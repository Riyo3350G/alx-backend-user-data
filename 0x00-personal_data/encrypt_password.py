#!/usr/bin/env python3
"""Encrypting passwords Module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ function that expects one string argument
    name password and returns a salted, hashed password
    , which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ function that expects a hashed_password bytes
    and a password string arguments and returns a boolean.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
