from functools import wraps
from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)

from extensions import db
from models.user_model import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        # Ensure JWT exists
        verify_jwt_in_request()

        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({
                "error": "Missing token identity"
            }), 401

        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        if user.role != "admin":
            return jsonify({
                "error": "Admin access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper