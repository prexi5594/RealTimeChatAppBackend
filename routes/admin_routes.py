from flask import Blueprint, jsonify

from middleware.auth_middleware import token_required
from utils.decorators import admin_required

from models.user_model import User
from models.message_model import Message
from models.room_model import Room

from extensions import db


admin_bp = Blueprint("admin", __name__)


# =========================
# GET ALL USERS
# =========================
@admin_bp.route("/admin/users", methods=["GET"])
@token_required
@admin_required
def get_users():

    users = User.query.all()

    data = []

    for user in users:
        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_banned": user.is_banned
        })

    return jsonify(data)


# =========================
# BAN USER
# =========================
@admin_bp.route("/admin/ban/<int:user_id>", methods=["POST"])
@token_required
@admin_required
def ban_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.is_banned = True

    db.session.commit()

    return jsonify({
        "message": "User banned"
    })


# =========================
# UNBAN USER
# =========================
@admin_bp.route("/admin/unban/<int:user_id>", methods=["POST"])
@token_required
@admin_required
def unban_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.is_banned = False

    db.session.commit()

    return jsonify({
        "message": "User unbanned"
    })


# =========================
# GET ALL MESSAGES
# =========================
@admin_bp.route("/admin/messages", methods=["GET"])
@token_required
@admin_required
def get_messages():

    messages = Message.query.all()

    data = []

    for message in messages:
        data.append({
            "id": message.id,
            "content": message.content
        })

    return jsonify(data)


# =========================
# DELETE MESSAGE
# =========================
@admin_bp.route(
    "/admin/messages/<int:message_id>",
    methods=["DELETE"]
)
@token_required
@admin_required
def delete_message(message_id):

    message = Message.query.get(message_id)

    if not message:
        return jsonify({
            "message": "Message not found"
        }), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({
        "message": "Message deleted"
    })


# =========================
# GET ALL ROOMS
# =========================
@admin_bp.route("/admin/rooms", methods=["GET"])
@token_required
@admin_required
def get_rooms():

    rooms = Room.query.all()

    data = []

    for room in rooms:
        data.append({
            "id": room.id,
            "name": room.name
        })

    return jsonify(data)


# =========================
# DELETE ROOM
# =========================
@admin_bp.route(
    "/admin/rooms/<int:room_id>",
    methods=["DELETE"]
)
@token_required
@admin_required
def delete_room(room_id):

    room = Room.query.get(room_id)

    if not room:
        return jsonify({
            "message": "Room not found"
        }), 404

    db.session.delete(room)
    db.session.commit()

    return jsonify({
        "message": "Room deleted"
    })


# =========================
# REPORTS
# =========================
@admin_bp.route("/admin/reports", methods=["GET"])
@token_required
@admin_required
def get_reports():

    return jsonify([
        {
            "id": 1,
            "reason": "Spam",
            "status": "pending"
        }
    ])