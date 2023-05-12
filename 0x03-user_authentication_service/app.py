#!/usr/bin/env python3
""" Basic Flask app """

from auth import Auth
from flask import Flask, jsonify, request


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """
    Flask app that has a single GET route ("/")
    Return:
        JSON payload of the form (using flask.jsonify)
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    Implements the POST /users route
    If user doesn't exist, registers new user with provided email & password
    Return:
        JSON payload with a success message and user's email.
        Or 400 error and a JSON payload with an error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify(email=user.email, message='user created')
    except ValueError:
        return jsonify(message='email already registered'), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
