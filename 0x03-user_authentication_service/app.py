#!/usr/bin/env python3
"""app flask implementation """
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
Auth = Auth()


@app.route("/")
def welcome():
    """Welcome function"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register():
    """register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = Auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """handling login"""
    email = request.form.get("email")
    password = request.form.get("password")
    if Auth.valid_login(email, password):
        session_gen = Auth.create_session(email)
        resp = make_response("Setting cookie")
        resp.set_cookie("session_id", session_gen)
        return jsonify({"email": email, "message": "logged in"})
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
