#!/usr/bin/env python3
""" Module of Session authentication views
"""
from flask import jsonify, abort, request, session
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - a session_id
    """
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session_id = auth.create_session(user_id=user.id)
        session_name = getenv('SESSION_NAME')
        session[session_name] = session_id
        return user.to_json()
