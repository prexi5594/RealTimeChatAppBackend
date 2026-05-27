import os
import random
from datetime import datetime, timedelta, timezone

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_mail import Mail, Message as MailMessage  # Alias to avoid conflict with your Message
# Alias Flask-Mail's Message as MailMessage to avoid collision with your chat model
from flask_mail import Message as MailMessage, Mail
from dotenv import load_dotenv

from config import Config
from extensions import db, jwt, mail

from models.user_model import User
from models.room_model import Room
# Keep your chat model named Message
from models.message_model import Message 

from routes.admin_routes import admin_bp

from werkzeug.security import generate_password_hash, check_password_hash


# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# APP SETUP
# =========================
app = Flask(__name__)
app.config.from_object(Config)

# =========================
# EXTENSIONS INIT
# =========================
db.init_app(app)
jwt.init_app(app)
mail.init_app(app)

CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})
app.register_blueprint(admin_bp, url_prefix="/admin")

# =========================
# CREATE TABLES + ADMIN
# =========================
with app.app_context():
    db.create_all()
    
    required_rooms = [
        {"id": 1, "name": "General"},
        {"id": 2, "name": "Sports"},
        {"id": 3, "name": "Politics"},
        {"id": 4, "name": "Fashion"}
    ]

    for room_data in required_rooms:
        room = Room.query.get(room_data["id"])
        if not room:
            new_room = Room(id=room_data["id"], name=room_data["name"])
            db.session.add(new_room)
    
    db.session.commit()
    print("Database rooms synchronized with frontend IDs!")
    
    User.query.filter_by(email="qchatadmin@gmail.com").delete()
    db.session.commit()

    admin = User.query.filter_by(email="qchatadmin@gmail.com").first()

    if not admin:
        hashed_password = generate_password_hash("RVP@2026")
        
        admin = User(
            email="qchatadmin@gmail.com",
            username="Admin",
            password=hashed_password,
            role="admin",
            is_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print("ADMIN CREATED WITH HASHED PASSWORD")

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify({"message": "Backend running"}), 200


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        if existing_user.is_verified:
            return jsonify({"error": "Email already registered and verified"}), 400

        # user exists but NOT verified → resend OTP
        otp = str(random.randint(100000, 999999))
        existing_user.otp_code = otp
        db.session.commit()

        try:
            # Fixed typo 'recepients' -> 'recipients' and updated to MailMessage
            msg = MailMessage(
                "QuickChat OTP Code",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email]
            )
            msg.body = f"Your OTP code is: {otp}"
            
            mail.send(msg)
            return jsonify({"message": "OTP resent to existing user"}), 200

        except Exception as e:
            print("MAIL ERROR:", e)
            return jsonify({
                "message": "OTP generated but email failed",
                "error": str(e)
            }), 500

    # NEW USER
    otp = str(random.randint(100000, 999999))
    
    hashed_password = generate_password_hash(password)

    user = User(
        email=email,
        username=username,
        password=hashed_password,
        otp_code=otp,
        role="user",
        is_verified=False
    )

    db.session.add(user)
    db.session.commit()

    try:
        # Changed from ChatMessage (DB Model) to MailMessage (Flask-Mail)
        msg = MailMessage(
            "QuickChat OTP Code",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = f"Your OTP code is: {otp}"

        mail.send(msg)

        return jsonify({"message": "OTP sent"}), 201

    except Exception as e:
        print("MAIL ERROR:", e)
        return jsonify({
            "message": "User created but email failed",
            "error": str(e)
        }), 500


# =========================
# VERIFY OTP
# =========================
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()

    email = data.get("email")
    code = data.get("code")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.otp_code != code:
        return jsonify({"error": "Invalid OTP"}), 400

    user.is_verified = True
    user.otp_code = None
    db.session.commit()

    return jsonify({"message": "Verified successfully"}), 200


# =========================
# LOGIN
# =========================


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not user.is_verified:
        return jsonify({
            "error": "Email not verified",
            "needs_verification": True,
            "email": user.email
        }), 403

    # 🌟 GENERATE A REAL VALID JWT ACCESS TOKEN
    # We pass the user's ID as the identity, and store their role in custom claims
    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims={"role": user.role}
    )

    # Return the token string alongside the user object
    return jsonify({
        "message": "Login successful",
        "token": access_token,  # 🌟 Sending the real signed token to your frontend
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
    }), 200


# =========================
# GET MESSAGES
# =========================
@app.route("/messages/<int:room_id>", methods=["GET"])
def get_messages(room_id):
    # This automatically references your chat Message model correctly now
    messages = Message.query.filter_by(room_id=room_id).all()

    return jsonify([
        {
            "id": m.id,
            "username": m.username,
            "message": m.message,
            "room_id": m.room_id,
            "timestamp": m.timestamp.isoformat(),
            "isDeleted": m.is_deleted
        }
        for m in messages
    ]), 200


# =========================
# SEND MESSAGE
# =========================
@app.route("/messages", methods=["POST"])
def send_message():
    data = request.get_json()

    msg = Message(
        username=data.get("username"),
        message=data.get("message"),
        room_id=data.get("room_id"),
        timestamp=datetime.now(timezone.utc)
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({
        "message": "sent",
        "data": {
            "id": msg.id,
            "username": msg.username,
            "message": msg.message,
            "room_id": msg.room_id,
            "timestamp": msg.timestamp.isoformat()
        }
    }), 201


# =========================
# CREATE ROOM
# =========================
@app.route("/rooms", methods=["POST"])
def create_room():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        name = data.get("name")
        if not name or not name.strip():
            return jsonify({"error": "Room name is required"}), 400

        # Check if room already exists to prevent unique constraints errors
        existing_room = Room.query.filter_by(name=name.strip()).first()
        if existing_room:
            return jsonify({"error": "A chat room with that name already exists"}), 400

        # Create the new room row structure
        # (Add topic=data.get('topic') etc. here if your DB columns exist)
        new_room = Room(name=name.strip())

        db.session.add(new_room)
        db.session.commit()  # Ensure the session commits to generate the ID!

        # Return status 201 along with the actual generated row properties
        return jsonify({
            "message": "Room created successfully",
            "room": {
                "id": new_room.id,
                "name": new_room.name
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback transaction on failure
        print("SQL ERROR OCCURRED:", str(e))  # This will print the full error in your terminal!
        return jsonify({"error": "Internal server database error"}), 500


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
            "created_at": r.created_at.isoformat()
        }
        for r in rooms
    ]), 200


# =========================
# SOFT DELETE MESSAGE
# =========================
@app.route("/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    msg = Message.query.get(message_id)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    msg.is_deleted = True
    db.session.commit()

    return jsonify({"message": "deleted"}), 200


# =========================
# RESEND OTP
# =========================
@app.route("/resend-otp", methods=["POST"])
def resend_otp():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    otp = str(random.randint(100000, 999999))
    user.otp_code = otp
    db.session.commit()

    # Updated to use MailMessage to avoid class conflict
    msg = MailMessage()
    msg.subject = "QuickChat OTP Code (Resend)"
    msg.recipients = [email]
    msg.body = f"Your OTP code is: {otp}"
    msg.sender = app.config["MAIL_USERNAME"]
    
    try:
        mail.send(msg)
        return jsonify({"message": "OTP resent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# =========================
# DELETE ROOM
# =========================
@app.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    try:
        # Protect default/general channels from being deleted
        if room_id == 1:
            return jsonify({"error": "The primary channel cannot be deleted"}), 403

        room = Room.query.get(room_id)
        if not room:
            return jsonify({"error": "Room not found"}), 404

        
        db.session.delete(room)
        db.session.commit()

        return jsonify({"message": "Room deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print("DELETE ERROR:", str(e))
        return jsonify({"error": "Database error while deleting room"}), 500
    
    
    

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)