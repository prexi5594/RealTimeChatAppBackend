import jwt
from functools import wraps
from flask import request, jsonify
from config import Config

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 1. Properly pull the token from the header first
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"message": "Token is missing"}), 401
        
        try:
            # 2. Extract the token (Expected format: "Bearer <token>")
            token = auth_header.split(" ")[1]
            print(f"DEBUG: Received Token: {token}")

            # 3. Decode manually using your Config secret
            decoded = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )
            
            print(f"DEBUG: Decoded Payload: {decoded}")
            request.user = decoded
            
        except Exception as e:
            print(f"DEBUG: Token Error: {str(e)}")
            return jsonify({"message": "Invalid token"}), 401
            
        return fn(*args, **kwargs)
    return wrapper