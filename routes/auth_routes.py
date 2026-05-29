from flask import Blueprint, request, jsonify, current_app
from extensions import db, mail
from models.user_model import User

from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from utils.Helper import send_otp_email
from datetime import timedelta
import random


auth_bp = Blueprint("auth", __name__)


# =====================
# OTP GENERATOR
# =====================
def generate_otp():
    return str(random.randint(100000, 999999))


# =====================
# REGISTER (OTP FLOW)
# =====================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    # check existing user
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already exists"}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    otp = generate_otp()

    user = User(
        username=username,
        email=email,
        otp_code=otp,
        otp_verified=False,
        is_verified=False,
        role="user"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # send OTP email
    try:
        send_otp_email(mail, email, otp, current_app._get_current_object())
    except Exception as e:
        print("OTP EMAIL ERROR:", e)

    return jsonify({
        "message": "User created. Check email for OTP",
        "action": "verify-otp"
    }), 201


# =====================
# VERIFY OTP
# =====================
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json() or {}

    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({"error": "Missing fields"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.otp_verified:
        return jsonify({"message": "OTP already verified"}), 200

    if user.otp_code != otp:
        return jsonify({"error": "Invalid OTP"}), 400

    user.otp_verified = True
    user.is_verified = True
    user.otp_code = None

    db.session.commit()

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
        expires_delta=timedelta(days=7)
    )

    return jsonify({
        "message": "OTP verified successfully",
        "token": token,
        "user": user.to_dict()
    }), 200


# =====================
# LOGIN
# =====================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Wrong password"}), 401

    if not user.is_verified:
        return jsonify({
            "error": "Verify your account first",
            "action": "verify-otp"
        }), 403

    if user.is_banned:
        return jsonify({"error": "Your account is banned"}), 403

    user.is_online = True
    db.session.commit()

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
        expires_delta=timedelta(days=7)
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    }), 200


# =====================
# RESEND OTP
# =====================
@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    data = request.get_json() or {}

    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    otp = generate_otp()
    user.otp_code = otp

    db.session.commit()

    try:
        send_otp_email(mail, email, otp, current_app._get_current_object())
    except Exception as e:
        print("RESEND OTP ERROR:", e)

    return jsonify({
        "message": "OTP resent successfully",
        "action": "verify-otp"
    }), 200


# =====================
# PROFILE (JWT TEST)
# =====================
@auth_bp.route("/profile", methods=["GET"])
def profile():
    return jsonify({"message": "Auth routes working"}), 200