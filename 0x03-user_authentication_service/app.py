#!/usr/bin/env python3
""" Basic Flask app """

from auth import Auth
from flask import Flask, abort, jsonify, redirect, request


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
    user_mail = request.form.get('email')
    user_pwd = request.form.get('password')
    if not AUTH.valid_login(email=user_mail, password=user_pwd):
        abort(401)
    else:
        session_id = AUTH.create_session(user_mail)
        reply = jsonify(email=user_mail, message='logged in')
        reply.set_cookie("session_id", session_id)
        return reply


@app.route('/session', methods=['GET'], strict_slashes=False)
def logout() -> str:
    """
    Logout function that responds to the GET /sessions route
    """
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ User profile """
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    return jsonify(email=user.email), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token_route() -> str:
    """
    Responds to POST /reset_password route
    Return:
        403 status code if email not registered
        Generate token & respond with 200 HTTP status if exists
    """
    user_mail = request.form.get('email')
    is_registered = AUTH.create_session(user_mail)
    if not is_registered:
        abort(403)
    token = AUTH.get_reset_password_token(user_mail)
    return jsonify({"email": user_mail, "reset_token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
