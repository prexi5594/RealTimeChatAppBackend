from flask import Blueprint, request, jsonify

from db import db
from models.message_model import Message

message_bp = Blueprint('messages', __name__)

# Send message
@message_bp.route('/messages', methods=['POST'])
def send_message():

    data = request.get_json()

    username = data.get('username')
    room = data.get('room')
    content = data.get('content')

    new_message = Message(
        username=username,
        room=room,
        content=content
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message sent"})


# Get messages by room
@message_bp.route('/messages/<room>', methods=['GET'])
def get_messages(room):

    messages = Message.query.filter_by(room=room).all()

    message_list = []

    for msg in messages:
        message_list.append({
            "username": msg.username,
            "content": msg.content,
            "timestamp": msg.timestamp
        })

    return jsonify(message_list)