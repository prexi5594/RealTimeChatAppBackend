import jwt

from functools import wraps
from flask import request, jsonify

from config import Config


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({
                "message": "Token missing"
            }), 401

        try:
            # Remove Bearer
            token = token.split(" ")[1]

            decoded = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = decoded

        except Exception:
            return jsonify({
                "message": "Invalid token"
            }), 401

        return f(*args, **kwargs)

    return decorated