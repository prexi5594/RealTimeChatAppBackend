from flask import Blueprint, request, jsonify
from db import db
from mail import mail
from models.user_model import User
from Utils.Helper import hash_password, check_password

from flask_jwt_extended import (
    create_access_token,
    decode_token
)

from flask_mail import Message
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)

# ================= REGISTER =================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    full_name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        username=full_name,
        email=email,
        password=hash_password(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password(password, user.password):
        return jsonify({"error": "Invalid password"}), 401

    token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=1)
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200


# ================= FORGOT PASSWORD =================
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=15)
    )

    reset_link = f"http://localhost:5173/reset-password?token={token}"

    msg = Message(
        subject="Password Reset",
        recipients=[email],
        body=f"Click to reset password:\n\n{reset_link}"
    )

    mail.send(msg)

    return jsonify({"message": "Reset email sent"}), 200


# ================= RESET PASSWORD =================
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()

    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Missing data"}), 400

    try:
        decoded = decode_token(token)
        user_id = decoded["sub"]

        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        user.password = hash_password(new_password)
        db.session.commit()

        return jsonify({"message": "Password updated"}), 200

    except Exception:
        return jsonify({"error": "Invalid or expired token"}), 400