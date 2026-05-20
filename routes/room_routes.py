from flask import Blueprint, request, jsonify

from extensions import db
from models.room_model import Room

room_bp = Blueprint('rooms', __name__, url_prefix="/rooms")

@room_bp.route("", methods=['POST'])
def create_room():

    data = request.get_json()

    room_name = data.get('name')

    existing_room = Room.query.filter_by(name=room_name).first()

    if existing_room:
        return jsonify({"message": "Room already exists"}), 400

    new_room = Room(name=room_name)

    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room created successfully"})



@room_bp.route("", methods=['GET'])
def get_rooms():

    rooms = Room.query.all()

    room_list = []

    for room in rooms:
        room_list.append({
            "id": room.id,
            "name": room.name
        })

    return jsonify(room_list)