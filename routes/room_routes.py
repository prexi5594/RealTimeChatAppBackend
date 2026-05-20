from flask import Blueprint, request, jsonify
from db import db
from models.room_model import Room

room_bp = Blueprint('rooms', __name__, url_prefix="/rooms")

@room_bp.route("", methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('name')

    if Room.query.filter_by(name=room_name).first():
        return jsonify({"message": "Room already exists"}), 400

    db.session.add(Room(name=room_name))
    db.session.commit()

    return jsonify({"message": "Room created successfully"}), 201


@room_bp.route("", methods=['GET'])
def get_rooms():
    rooms = Room.query.all()

    return jsonify([
        {"id": r.id, "name": r.name}
        for r in rooms
    ]), 200