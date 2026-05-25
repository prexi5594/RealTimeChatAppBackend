from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)

# ===== CORS (IMPORTANT for React) =====
CORS(app, origins=["http://localhost:5173", "http://localhost:5175"])

# ===== JWT CONFIG =====
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

# ===== SIMPLE IN-MEMORY STORAGE (TEST ONLY) =====
users = []
messages = []

# ===== HEALTH CHECK =====
@app.route("/")
def home():
    return jsonify({"message": "Backend running"}), 200

# ===== REGISTER =====
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    # check if user exists
    for user in users:
        if user["email"] == email:
            return jsonify({"error": "User already exists"}), 400

    users.append({
        "email": email,
        "password": password
    })

    return jsonify({"message": "User registered successfully"}), 201


# ===== LOGIN =====
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
    "message": "Login successful",
    "user": {
        "email": email,
        "username": email.split("@")[0]
    }
}), 200

    return jsonify({"error": "Invalid credentials"}), 401


# ===== GET MESSAGES BY ROOM =====
@app.route("/messages/<room>", methods=["GET"])
def get_messages(room):
    room_messages = [
        msg for msg in messages if msg["room"] == room
    ]
    return jsonify(room_messages), 200


# ===== SEND MESSAGE =====
@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()

    message = {
        "username": data.get("username"),
        "message": data.get("message"),
        "room": data.get("room")
    }

    messages.append(message)

    return jsonify({
        "success": True,
        "message": message
    }), 201
    
# ==========Get Rooms===============
@app.route("/rooms", methods=["GET"])
def get_rooms():
    return jsonify(rooms)

# ==========Create Room===============
@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.get_json()
    room_name = data.get("name")

    if not room_name:
        return jsonify({"error": "Room name is required"}), 400

    # Check if room already exists
    for room in rooms:
        if room["name"] == room_name:
            return jsonify({"error": "Room already exists"}), 400

    new_room = {
        "name": room_name,
        "created_at": datetime.utcnow().isoformat()
    }
    rooms.append(new_room)

    return jsonify({
        "message": "Room created successfully",
        "room": new_room
    }), 201
    
# ===== SOFT DELETE MESSAGE =====    
@app.route("/messages/<int:message_id>", methods=["PATCH"])
def delete_message(message_id):
    message = Message.query.get(message_id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    message.is_deleted = True
    message.message = "Message deleted"

    db.session.commit()

    return jsonify({"success": True})
    

# ===== RUN SERVER =====
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )