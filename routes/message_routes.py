from flask import Blueprint, request, jsonify
from db import db
from models.message_model import Message
from models.room_model import Room

message_bp = Blueprint("messages", __name__)


# =========================
# SEND MESSAGE
# =========================
@message_bp.route("/messages", methods=["POST"])
def send_message():

    try:
        data = request.get_json()

        username = data.get("username")
        room_name = data.get("room")
        text = data.get("text")

        if not username or not room_name or not text:
            return jsonify({"error": "Missing fields"}), 400

        # find room by name
        room = Room.query.filter_by(name=room_name).first()

        if not room:
            return jsonify({"error": "Room not found"}), 404

        new_message = Message(
            user_id=1,  # temporary (no auth yet)
            room_id=room.id,
            message=text
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({"message": "Message sent successfully"}), 201

    except Exception as e:
        print("SEND ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# =========================
# GET MESSAGES
# =========================
@message_bp.route("/messages", methods=["GET"])
def get_messages():

    room_name = request.args.get("room")

    if not room_name:
        return jsonify([]), 200

    room = Room.query.filter_by(name=room_name).first()

    if not room:
        return jsonify([]), 200

    messages = Message.query.filter_by(room_id=room.id).all()

    return jsonify([
        {
            "id": m.id,
            "username": "User",
            "room": room_name,
            "content": m.message,
            "timestamp": m.timestamp
        }
        for m in messages
    ]), 200