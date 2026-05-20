from flask import Blueprint, request, jsonify
<<<<<<< HEAD
from db import db
=======
from extensions import db
>>>>>>> 422b5bc (final changes)
from models.message_model import Message

message_bp = Blueprint("messages", __name__)

<<<<<<< HEAD
# =========================
# SEND MESSAGE (FIXED)
# =========================
@message_bp.route("/messages", methods=["POST"])
=======

# =========================
# SEND MESSAGE
# =========================
@message_bp.route('/messages', methods=['POST'])
>>>>>>> 422b5bc (final changes)
def send_message():
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        room_id = data.get("room_id")
        text = data.get("message")

<<<<<<< HEAD
        if not room_id or not text:
            return jsonify({"error": "Missing fields"}), 400
=======
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    room = data.get('room')
    content = data.get('content')   # ✅ OPTION B

    # validation
    if not username or not room or not content:
        return jsonify({"error": "Missing username, room, or content"}), 400
>>>>>>> 422b5bc (final changes)

        new_message = Message(
            user_id=user_id if user_id else 1,
            room_id=room_id,
            message=text
        )

<<<<<<< HEAD
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
=======
    try:
        db.session.add(new_message)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Message sent successfully"}), 201

@message_bp.route('/messages/<room>', methods=['GET'])
def get_messages(room):
>>>>>>> 422b5bc (final changes)

    if not room_id:
        return jsonify([]), 200

    messages = Message.query.filter_by(room_id=room_id).all()

<<<<<<< HEAD
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
=======
    for msg in messages:
        message_list.append({
            "username": msg.username,
            "room": msg.room,
            "content": msg.content,
            "timestamp": msg.timestamp
        })

    return jsonify(message_list), 200
>>>>>>> 422b5bc (final changes)
