from flask import Blueprint, request, jsonify
from models.message_model import Message
from models.room_model import Room
from extensions import db
message_bp = Blueprint("messages", __name__, url_prefix="/messages")

@message_bp.route("", methods=["POST"])
def send_message():
    data = request.get_json()

    user_id = data.get("user_id", 1)
    room_id = data.get("room_id")
    text = data.get("message")

    if not room_id or not text:
        return jsonify({"error": "Missing fields"}), 400

    new_message = Message(
        user_id=user_id,
        room_id=room_id,
        message=text
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message sent"}), 201



@message_bp.route("/room/<int:room_id>", methods=["GET"])
def get_messages(room_id):
    room = Room.query.get(room_id)
    if not room:
        return {"error": "Room not found"}, 404

    messages = Message.query.filter_by(room_id=room.id).all()

    return jsonify([
        {
            "id": m.id,
            "message": m.message,
            "username": m.username,
            "room": room.name,
            "timestamp": str(m.timestamp)
        }
        for m in messages
    ])
@message_bp.route("/messages", methods=["POST"])
def send_message():
    data = request.get_json()

    message = data.get("message")
    username = data.get("username")
    room_name = data.get("room")

    if not message or not username or not room_name:
        return {"error": "Missing fields"}, 400

    room = Room.query.filter_by(name=room_name).first()

    if not room:
        return {"error": "Room not found"}, 404

    new_msg = Message(
        message=message,
        username=username,
        room_id=room.id
    )

    db.session.add(new_msg)
    db.session.commit()

    return {"message": "Message sent"}, 201