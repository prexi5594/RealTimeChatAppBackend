from flask import Blueprint, request, jsonify

from db import db
from models.message_model import Message


message_bp = Blueprint("messages", __name__)


# SEND MESSAGE
@message_bp.route("/messages", methods=["POST"])
def send_message():

    data = request.get_json()

    user_id = data.get("user_id")
    room_id = data.get("room_id")
    message = data.get("message")

    if not user_id or not room_id or not message:
        return jsonify({
            "message": "Missing fields"
        }), 400

    new_message = Message(
        user_id=user_id,
        room_id=room_id,
        message=message
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "message": "Message sent successfully"
    }), 201


# GET ROOM MESSAGES
@message_bp.route("/messages/<int:room_id>", methods=["GET"])
def get_messages(room_id):

    messages = Message.query.filter_by(
        room_id=room_id
    ).all()

    message_list = []

    for msg in messages:
        message_list.append({
            "id": msg.id,
            "user_id": msg.user_id,
            "room_id": msg.room_id,
            "message": msg.message,
            "timestamp": msg.timestamp
        })

    return jsonify(message_list), 200