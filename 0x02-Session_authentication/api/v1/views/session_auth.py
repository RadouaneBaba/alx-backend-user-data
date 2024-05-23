#!/usr/bin/env python3
"""doc doc doc"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def view_session_login() -> str:
    """
    POST /api/v1/auth_session/login
    """
    email = request.get("email")
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.get("password")
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        user_list = User.search({"email": email})

        if not user_list:
            return jsonify({"error": "no user found for this email"}), 404

        user = user_list[0]
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth

        session_id = auth.create_session(user.id)
        resp = jsonify(user.to_json())
        resp.set_cookie(getenv("SESSION_NAME"), session_id)
        return resp
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
