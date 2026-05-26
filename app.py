import os
import random  # Added: Needed to generate 6-digit verification numbers
from flask import Flask, request, jsonify, redirect
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables from your local .env file
load_dotenv()

app = Flask(__name__)

# ===== CORS CONFIGURATION =====
CORS(app, origins=[
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "http://172.31.149.133:5173"
])

# ===== JWT CONFIG =====
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

# ===== EMAIL SMTP CONFIGURATION =====
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

# 🔍 DEBUG PRINTS
print("--- ENVIRONMENT CHECK ---")
print("DEBUG - MAIL_USERNAME LOADED:", app.config["MAIL_USERNAME"])
print("DEBUG - MAIL_PASSWORD LOADED:", "Key exists!" if app.config["MAIL_PASSWORD"] else "MISSING/NONE")
print("------------------------")

mail = Mail(app)

# ===== SIMPLE IN-MEMORY STORAGE =====
users = []
messages = []
rooms = [] 

# ===== HEALTH CHECK =====
@app.route("/")
def home():
    return jsonify({"message": "Backend running"}), 200

# ===== REGISTER (Sends 6-Digit OTP Code like Instagram) =====
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    # check if user exists
    for user in users:
        if user["email"] == email:
            return jsonify({"error": "User already exists"}), 400

    # Generate a secure 6-digit random number string
    otp_code = str(random.randint(100000, 999999))

    # Save user with verification disabled and cache their unique OTP
    users.append({
        "email": email,
        "password": password,
        "username": username,
        "is_verified": False,
        "otp": otp_code
    })

    try:
        msg = Message(
            "Your Quickchat Verification Code",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = f"Welcome to Quickchat! Your 6-digit verification code is: {otp_code}"
        msg.html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
                <h2 style="color: #0052CC; text-align: center;">Welcome to Quickchat!</h2>
                <p>Thank you for signing up. Use the verification code below to activate your account:</p>
                <div style="background-color: #f4f6f9; padding: 15px; text-align: center; border-radius: 5px; margin: 20px 0;">
                    <h1 style="color: #333; letter-spacing: 5px; margin: 0; font-size: 32px;">{otp_code}</h1>
                </div>
                <p style="color: #666; font-size: 12px; text-align: center;">This code is valid for temporary verification loops.</p>
            </div>
        """
        mail.send(msg)
        return jsonify({"message": "Verification code sent! Check your inbox."}), 201
    except Exception as e:
        print("Mail Send Exception Details:", str(e))
        return jsonify({"error": "Failed to send verification email. Check your .env setup."}), 500

# ===== NEW ROUTE: VERIFY OTP CODE =====
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json() or {}
    email = data.get("email")
    user_code = data.get("code")

    if not email or not user_code:
        return jsonify({"error": "Email and verification code are required"}), 400

    for user in users:
        if user["email"] == email:
            if user["otp"] == str(user_code).strip():
                user["is_verified"] = True
                return jsonify({"message": "Email verified successfully!"}), 200
            return jsonify({"error": "Incorrect verification code"}), 400

    return jsonify({"error": "User registration record not found"}), 404

# ===== LOGIN (Blocks unverified users) =====
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    for user in users:
        if user["email"] == email and user["password"] == password:
            if not user.get("is_verified", False):
                return jsonify({"error": "Please verify your email address before logging in."}), 403
                
            return jsonify({
                "message": "Login successful",
                "user": {
                    "email": email,
                     "username": user["username"]
                }
            }), 200

    return jsonify({"error": "Invalid credentials"}), 401

# ===== GET MESSAGES BY ROOM =====
@app.route("/messages/<room>", methods=["GET"])
def get_messages(room):
    room_messages = [msg for msg in messages if msg["room"] == room]
    return jsonify(room_messages), 200

# ===== SEND MESSAGE =====
@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json() or {}
    message = {
        "username": data.get("username"),
        "message": data.get("message"),
        "room": data.get("room")
    }
    messages.append(message)
    return jsonify({"success": True, "message": message}), 201
    
# ========== GET ROOMS ===============
@app.route("/rooms", methods=["GET"])
def get_rooms():
    return jsonify(rooms)

# ========== CREATE ROOM ===============
@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json() or {}
    room_name = data.get("name")

    if not room_name:
        return jsonify({"error": "Room name is required"}), 400

    for room in rooms:
        if room["name"] == room_name:
            return jsonify({"error": "Room already exists"}), 400

    new_room = {
        "name": room_name,
        "created_at": datetime.utcnow().isoformat()
    }
    rooms.append(new_room)
    return jsonify({"message": "Room created successfully", "room": new_room}), 201
    
# ==========Delete Message (Soft Delete)===============
@app.route("/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):

    global messages

    # Check if message exists
    if message_id < 0 or message_id >= len(messages):
        return jsonify({
            "error": "Message not found"
        }), 404

    # Soft delete
    messages[message_id]["message"] = "Message deleted"
    messages[message_id]["isDeleted"] = True

    return jsonify({
        "status": "deleted"
    }), 200
 
if __name__ == "__main__":
    app.run(debug=True) 
