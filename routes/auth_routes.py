import jwt

from flask import current_app

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from models.user_model import User
from extensions import db, mail

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_mail import Message

from itsdangerous import (
    URLSafeTimedSerializer,
    SignatureExpired
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from datetime import timedelta


auth_bp = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    # CHECK EXISTING EMAIL
    existing_email = User.query.filter_by(email=email).first()

    if existing_email:

        # USER EXISTS BUT NOT VERIFIED
        if not existing_email.is_verified:

            serializer = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"]
            )

            token = serializer.dumps(
                email,
                salt="verify-email"
            )

            link = f"https://realtimechatapp2-vgnu.onrender.com/verify/{token}"

            msg = Message(
                "Verify QuickChat Account",
                sender=current_app.config["MAIL_USERNAME"],
                recipients=[email]
            )

            msg.body = (
                f"Click the link to verify your account:\n{link}"
            )

            mail.send(msg)

            return jsonify({
                "message":
                "Verification email resent"
            }), 200

        return jsonify({
            "error": "Email already exists"
        }), 409

    # CHECK USERNAME
    if User.query.filter_by(username=username).first():
        return jsonify({
            "error": "Username already exists"
        }), 409

    # CREATE USER
    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    # SEND VERIFICATION EMAIL
    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    token = serializer.dumps(
        email,
        salt="verify-email"
    )

    link = f"https://realtimechatapp2-vgnu.onrender.com/verify/{token}"

    msg = Message(
        "Verify QuickChat Account",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = (
        f"Click the link to verify your account:\n{link}"
    )

    mail.send(msg)

    return jsonify({
        "message":
        "Check your email to verify account"
    }), 201


# =========================
# VERIFY EMAIL
# =========================
@auth_bp.route("/verify/<token>", methods=["GET"])
def verify(token):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:
        email = serializer.loads(
            token,
            salt="verify-email",
            max_age=3600
        )

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user.is_verified = True
        db.session.commit()

        return jsonify({
            "message": "Email verified successfully"
        })

    except SignatureExpired:
        return jsonify({
            "error": "Verification link expired"
        }), 400

    except Exception as e:
        print(e)
        return jsonify({
            "error": "Invalid token"
        }), 400


# =========================
# LOGIN (JWT)
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

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
            "error": "Verify your email first"
        }), 403

    if user.is_banned:
        return jsonify({
            "error": "Your account is banned"
        }), 403

    # ONLY mark online AFTER all checks pass
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
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_banned": user.is_banned
        }
    }), 200
    
    
# =========================
# FORGOT PASSWORD
# =========================
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email required"}), 400

    user = User.query.filter_by(email=email).first()

    # Always respond same way (security best practice)
    if not user:
        return jsonify({
            "message": "If email exists, reset link sent"
        }), 200

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    token = serializer.dumps(email, salt="reset-password")

    reset_link = f"https://realtimechatapp2-vgnu.onrender.com/reset-password/{token}"

    msg = Message(
        "Reset Password - QuickChat",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = f"Click to reset your password:\n{reset_link}"

    mail.send(msg)

    return jsonify({
        "message": "Reset email sent"
    }), 200


# =========================
# RESET PASSWORD
# =========================
@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):

    try:
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        email = serializer.loads(
            token,
            salt="reset-password",
            max_age=3600
        )

        data = request.get_json()
        new_password = data.get("password")

        if not new_password:
            return jsonify({"error": "Password required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({
            "message": "Password updated successfully"
        }), 200

    except SignatureExpired:
        return jsonify({
            "error": "Reset link expired"
        }), 400

    except Exception as e:
        print(e)
        return jsonify({
            "error": "Invalid token"
        }), 400


# =========================
# PROTECTED PROFILE
# =========================
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_verified": user.is_verified,
        "is_online": user.is_online
    }), 200