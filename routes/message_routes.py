from flask import Blueprint, request, jsonify
from db import db
from models.message_model import Message

message_bp = Blueprint("messages", __name__)

# =========================
# SEND MESSAGE (FIXED)
# =========================
@message_bp.route("/messages", methods=["POST"])
def send_message():
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        room_id = data.get("room_id")
        text = data.get("message")

        if not room_id or not text:
            return jsonify({"error": "Missing fields"}), 400

        new_message = Message(
            user_id=user_id if user_id else 1,
            room_id=room_id,
            message=text
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({"message": "Message sent"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# GET MESSAGES (FIXED)
# =========================
@message_bp.route("/messages", methods=["GET"])
def get_messages():
    room_id = request.args.get("room")

    if not room_id:
        return jsonify([]), 200

    messages = Message.query.filter_by(room_id=room_id).all()

    return jsonify([
        {
            "id": m.id,
            "username": f"User {m.user_id}",
            "room_id": m.room_id,
            "content": m.message,
            "timestamp": str(m.timestamp)
        }
        for m in messages
    ]), 200