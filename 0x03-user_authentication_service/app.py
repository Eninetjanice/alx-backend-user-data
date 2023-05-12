#!/usr/bin/env python3
""" Basic Flask app """

from auth import Auth
from flask import Flask, abort, jsonify, request


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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Login function that responds to the POST /sessions route
    """
    user_email = request.form['email']
    user_pwd = request.form['password']
    if not AUTH.valid_login(email=user_email, password=user_pwd):
        abort(401)
    else:
        AUTH.create_session(user_email)
        return jsonify(email=user_email, message='logged in')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
