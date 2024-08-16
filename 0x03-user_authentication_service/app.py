#!/usr/bin/env python3
"""
Flask app that defines API routes
"""
from flask import Flask, request, jsonify, abort, \
    make_response, redirect, url_for
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    Welcome page of the API
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    Register a new user.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    create a new session for a user, store the session ID as a cookie

    Returns:
    JSON payload of the form
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(
            jsonify({"email": email, "message": "logged in"})
            )
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    destroy the session for the user, remove the session ID from the cookie

    Returns:
    JSON payload of the form
    """
    session_id = request.cookies.get("session_id")

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            response = make_response(redirect(url_for('home')))
            response.delete_cookie("session_id")
            return response
    else:
        abort(403)


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile():
    """
    get user profile
    """
    session_id = request.cookies.get("session_id")

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    else:
        abort(403)


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    get a reset password token for a user
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
