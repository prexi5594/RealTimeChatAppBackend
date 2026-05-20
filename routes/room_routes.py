from flask import Blueprint, request, jsonify
<<<<<<< HEAD
from db import db
=======

from extensions import db
>>>>>>> 422b5bc (final changes)
from models.room_model import Room

room_bp = Blueprint('rooms', __name__)

@room_bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('name')

    if Room.query.filter_by(name=room_name).first():
        return jsonify({"message": "Room already exists"}), 400

    db.session.add(Room(name=room_name))
    db.session.commit()

    return jsonify({"message": "Room created successfully"}), 201


<<<<<<< HEAD
=======

>>>>>>> 422b5bc (final changes)
@room_bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()

    return jsonify([
        {"id": r.id, "name": r.name}
        for r in rooms
    ]), 200