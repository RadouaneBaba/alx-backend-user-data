#!/usr/bin/env python3
"""app flask implementation """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
