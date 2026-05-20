from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user_model import User

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():

    users = User.query.all()

    user_list = []

    for user in users:

        user_list.append({
            "id": user.id,
            "username": user.username
        })

    return jsonify(user_list), 200


@user_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):

    user = User.query.get(id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 200