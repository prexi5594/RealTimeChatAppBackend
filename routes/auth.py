from models.user_model import User
from extensions import db, mail
from flask_jwt_extended import create_access_token

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from utils.Helper import send_otp_email

import random


def generate_otp():
    return str(
        random.randint(
            100000,
            999999
        )
    )


auth_bp = Blueprint(
    "auth",
    __name__
)


# =====================
# REGISTER
# =====================
@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = (
        request.get_json()
        or {}
    )

    username = data.get(
        "username"
    )

    email = data.get(
        "email"
    )

    password = data.get(
        "password"
    )

    if (
        not username
        or not email
        or not password
    ):
        return jsonify({
            "error":
            "Missing fields"
        }), 400

    existing_email = (
        User.query
        .filter_by(
            email=email
        )
        .first()
    )

    if existing_email:
        return jsonify({
            "error":
            "Email already exists"
        }), 409

    existing_username = (
        User.query
        .filter_by(
            username=username
        )
        .first()
    )

    if existing_username:
        return jsonify({
            "error":
            "Username already exists"
        }), 409

    is_first_user = (
        User.query.count()
        == 0
    )

    otp = (
        generate_otp()
    )

    user = User(
        username=username,

        email=email,

        role=(
            "admin"
            if is_first_user
            else "user"
        ),

        otp_code=otp,

        otp_verified=False,

        is_verified=False
    )

    user.set_password(
        password
    )

    db.session.add(
        user
    )

    db.session.commit()

    # SEND OTP EMAIL
    try:
        send_otp_email(mail, email, otp, current_app)
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        # Continue even if email fails - user can request resend

    return jsonify({

        "message":
        "User created. Check your email for OTP",

        "role":
        user.role,

        "next":
        "Verify OTP",

        "action":
        "verify-otp"

    }), 201


# =====================
# VERIFY OTP
# =====================

@auth_bp.route(
    "/verify-otp",
    methods=["POST"]
)
def verify_otp():

    data = request.get_json() or {}

    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({
            "error": "Missing fields"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    if user.otp_verified:
        return jsonify({
            "message": "OTP already verified"
        }), 200

    if user.otp_code != otp:
        return jsonify({
            "error": "Invalid OTP"
        }), 400

    # VERIFY USER
    user.otp_verified = True
    user.is_verified = True
    user.otp_code = None

    db.session.commit()

    # CREATE JWT TOKEN
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "message": "OTP verified successfully",
        "token": access_token,
        "user": user.to_dict()
    }), 200


# =====================
# RESEND OTP
# =====================


@auth_bp.route(
    "/resend-otp",
    methods=["POST"]
)
def resend_otp():

    data = request.get_json() or {}

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    if user.is_verified:
        return jsonify({
            "message": "Account already verified. Please login.",
            "action": "login"
        }), 200

    otp = generate_otp()
    user.otp_code = otp
    db.session.commit()

    try:
        send_otp_email(mail, email, otp, current_app)
    except Exception as e:
        print(f"Error resending OTP email: {str(e)}")

    return jsonify({
        "message": "Existing account found. OTP resent to your email.",
        "action": "verify-otp"
    }), 200