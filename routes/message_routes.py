from flask import Blueprint, request, jsonify
from extensions import db
from models.message_model import Message
from models.room_model import Room
from datetime import datetime
import pytz

# 1. Define Blueprint with prefix
message_bp = Blueprint("messages", __name__, url_prefix="/messages")

# 2. Explicit Routes
@message_bp.route("/<int:room_id>", methods=["GET"])
def get_messages(room_id):
    messages = Message.query.filter_by(
        room_id=room_id,
           
    ).all()

    return jsonify([
        {
            "id": m.id,
            "message": m.message,
            "username": m.username,
            "timestamp": m.timestamp.isoformat(),
            "is_deleted": m.is_deleted
        } for m in messages
    ]), 200

@message_bp.route("", methods=["POST", "OPTIONS"], strict_slashes=False)
def send_message():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    try:
        data = request.get_json()
        print("DEBUG DATA RECEIVED:", data)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        message = data.get("message")
        username = data.get("username")
        room_id = data.get("room_id")

        if not all([message, username, room_id]):
            return jsonify({"error": "Missing fields"}), 400

       
        room = Room.query.get(room_id)
        if not room:
            return jsonify({"error": "Room does not exist"}), 404

        new_msg = Message(
            message=message,
            username=username,
            room_id=room_id,
            timestamp=datetime.now(pytz.timezone("Africa/Nairobi")),
            is_deleted=False
        )

        db.session.add(new_msg)
        db.session.commit()

        return jsonify({"status": "sent"}), 201

    except Exception as e:
        print("MESSAGE ERROR:", str(e))
        return jsonify({"error": "Internal server error"}), 500


# delete message route
@message_bp.route("/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    msg = Message.query.get(message_id)
    if not msg:
        return jsonify({"error": "Message not found"}), 404

    # Soft delete: mark as deleted instead of removing from DB
    msg.is_deleted = True
    db.session.commit()
    return jsonify({"status": "deleted"}), 200
