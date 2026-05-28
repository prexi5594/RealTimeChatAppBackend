from flask import Blueprint, request, jsonify
from extensions import db
from models.message_model import Message
from models.room_model import Room
from datetime import datetime, timezone

message_bp = Blueprint("messages", __name__, url_prefix="/messages")

# SEND MESSAGE
@message_bp.route("", methods=["POST"])
def send_message():
    data = request.get_json()

    message = data.get("message")
    username = data.get("username")
    room_id = data.get("room_id")

    if not all([message, username, room_id]):
        return jsonify({"error": "Missing fields"}), 400

    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    msg = Message(
        message=message,
        username=username,
        room_id=room_id,
        timestamp=datetime.now(timezone.utc),
        is_deleted=False
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"status": "sent"}), 201


# GET MESSAGES
@message_bp.route("/<int:room_id>", methods=["GET"])
def get_messages(room_id):

    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    messages = Message.query.filter_by(room_id=room_id).all()

    return jsonify([
        {
            "id": m.id,
            "message": m.message,
            "username": m.username,
            "timestamp": m.timestamp.isoformat(),
            "is_deleted": m.is_deleted
        }
        for m in messages
    ]), 200


# DELETE MESSAGE
@message_bp.route("/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):

    msg = Message.query.get(message_id)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    msg.is_deleted = True
    msg.message = "Message deleted"

    db.session.commit()

    return jsonify({"status": "deleted"}), 200