from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_mail import Mail, Message as MailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import random

from config import Config
from extensions import db

from models.user_model import User
from models.room_model import Room
from models.message_model import Message

from routes.auth_routes import auth_bp
from routes.room_routes import room_bp
from routes.message_routes import message_bp

# =========================
# APP SETUP
# =========================
app = Flask(__name__)
app.config.from_object(Config)


## blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(room_bp, url_prefix="/rooms")
app.register_blueprint(message_bp)

# Removed the trailing slash from the origin
CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost:5174",
        "https://realtimechatapp2-vgnu.onrender.com"
    ]}},
    supports_credentials=True,
    methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)


db.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)

# =========================
# INIT DB
# =========================
with app.app_context():
    db.create_all()


# =========================
# HOME
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend running"}), 200


# =========================
# CREATE ROOM
# =========================
@app.route("/rooms", methods=["POST"])
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

    room = Room(
        name=name,
        topic=topic,
        description=description
    )

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


# =========================
# GET ROOMS
# =========================
@app.route("/rooms", methods=["GET"])
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



# =========================
# DELETE MESSAGE (SOFT DELETE)
# =========================
@app.route("/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):

    msg = Message.query.get(message_id)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    msg.message = "Message deleted"
    msg.is_deleted = True

    db.session.commit()

    return jsonify({"message": "deleted"}), 200




# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)