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
    from api.v1.app import auth
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

        session_id = auth.create_session(user_id=user.id)
        session_name = getenv('SESSION_NAME')
        response = jsonify(user.to_json())
        response.set_cookie(session_name, session_id)
        return response

    @app_views.route('/auth_session/logout',
                     methods=['DELETE'],
                     strict_slashes=False)
    def logout() -> str:
        """ DELETE /api/v1/auth_session/logout
        Deletes a session and logout
        Return:
          - a success message
        """
        from api.v1.app import auth
        res = auth.destroy_session(request)
        if res is True:
            return jsonify({}), 200
        else:
            abort(404)
