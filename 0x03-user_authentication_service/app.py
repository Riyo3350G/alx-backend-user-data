#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """Welcome message from the API"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Create a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Login a user"""
    user_email = request.form.get('email', '')
    user_password = request.form.get('password', '')
    login = AUTH.valid_login(user_email, user_password)
    if not login:
        abort(401)
    resp = make_response(jsonify({"email": user_email,
                                  "message": "logged in"}))
    resp.set_cookie('session_id', AUTH.create_session(user_email))
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout a user"""
    session = request.cookies.get("session_id")
    if session is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """User profile"""
    session = request.cookies.get("session_id")
    if session is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Reset Password Token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
