from flask import Blueprint, jsonify, request
from middleware.auth_middleware import token_required
from utils.decorators import admin_required
from models.user_model import User
from models.message_model import Message
from models.room_model import Room
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =====================
# USERS
# =====================
@admin_bp.route("/users", methods=["GET", "OPTIONS"])
@token_required
@admin_required
def get_users():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    users = User.query.all()
    data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "is_banned": u.is_banned
        }
        for u in users
    ]
    return jsonify(data)


# =====================
# BAN USER
# =====================
@admin_bp.route("/ban/<int:user_id>", methods=["POST", "OPTIONS"])
@token_required
@admin_required
def ban_user(user_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_banned = True
    db.session.commit()
    return jsonify({"message": "User banned"})


# =====================
# UNBAN USER
# =====================
@admin_bp.route("/unban/<int:user_id>", methods=["POST", "OPTIONS"])
@token_required
@admin_required
def unban_user(user_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_banned = False
    db.session.commit()
    return jsonify({"message": "User unbanned"})


# =====================
# MESSAGES
# =====================
@admin_bp.route("/messages", methods=["GET", "OPTIONS"])
@token_required
@admin_required
def get_messages():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    messages = Message.query.all()
    data = [
        {"id": m.id, "content": m.content}
        for m in messages
    ]
    return jsonify(data)


@admin_bp.route("/messages/<int:message_id>", methods=["DELETE", "OPTIONS"])
@token_required
@admin_required
def delete_message(message_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    message = Message.query.get(message_id)
    if not message:
        return jsonify({"message": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"})


# =====================
# ROOMS
# =====================
@admin_bp.route("/rooms", methods=["GET", "OPTIONS"])
@token_required
@admin_required
def get_rooms():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    rooms = Room.query.all()
    data = [
        {"id": r.id, "name": r.name}
        for r in rooms
    ]
    return jsonify(data)


@admin_bp.route("/rooms/<int:room_id>", methods=["DELETE", "OPTIONS"])
@token_required
@admin_required
def delete_room(room_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    room = Room.query.get(room_id)
    if not room:
        return jsonify({"message": "Room not found"}), 404

    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted"})