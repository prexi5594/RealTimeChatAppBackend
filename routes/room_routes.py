from flask import Blueprint, request, jsonify
from extensions import db
from models.room_model import Room

room_bp = Blueprint("rooms", __name__, url_prefix="/rooms")

# CREATE ROOM
@room_bp.route("", methods=["POST"])
def create_room():
    data = request.get_json()

    name = data.get("name")
    topic = data.get("topic")
    description = data.get("description")

    if not name:
        return jsonify({"error": "Room name required"}), 400

    existing = Room.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Room already exists"}), 400

    room = Room(name=name, topic=topic, description=description)

    db.session.add(room)
    db.session.commit()

    return jsonify({
        "message": "Room created",
        "room": {
            "id": room.id,
            "name": room.name,
            "topic": room.topic,
            "description": room.description
        }
    }), 201


# GET ROOMS
@room_bp.route("", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()

    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "topic": r.topic,
            "description": r.description
        }
        for r in rooms
    ]), 200