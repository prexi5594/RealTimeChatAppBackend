import jwt
from functools import wraps
from flask import request, jsonify
from config import Config


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        # Allow CORS preflight requests
        if request.method == "OPTIONS":
            return "", 200

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token is missing"}), 401

        try:
            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = decoded

        except Exception as e:
            print("Token Error:", e)
            return jsonify({"message": "Invalid token"}), 401

        return fn(*args, **kwargs)

    return wrapper