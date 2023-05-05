#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
else:
    auth = Auth()

excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/', '/api/v1/auth_session/login/']


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Error handler for 401 Unauthorized status code. """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Error handler for 403 Forbidden status code. """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> str:
    """
    Filter each request that is handled by a function.
    """
    if auth is None:
        pass
    #  if not auth.require_auth(path, excluded_paths):
        #  return
    if not auth.require_auth(request.path, excluded_paths):
        pass
    elif auth.authorization_header(request) is None:
        abort(401)
    elif auth.current_user(request) is None:
        abort(403)
    elif auth.authorization_header(request) and auth.session_cookie(request):
        return None, abort(401)
    # update & assign result of auth.current_user(request)
    request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
