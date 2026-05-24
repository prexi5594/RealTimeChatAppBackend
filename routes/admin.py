from flask import Blueprint, jsonify

from flask_jwt_extended import jwt_required

from models.user_model import User
from models.message_model import Message
from extensions import db

from utils.decorators import admin_required


admin_bp = Blueprint("admin", __name__)


# =========================
# GET ALL USERS
# =========================
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# =========================
# DELETE USER
# =========================
@admin_bp.route("/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"})


# =========================
# ADMIN STATS
# =========================
@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
@admin_required
def admin_stats():

    total_users = User.query.count()
    online_users = User.query.filter_by(is_online=True).count()
    banned_users = User.query.filter_by(is_banned=True).count()

    return jsonify({
        "total_users": total_users,
        "online_users": online_users,
        "banned_users": banned_users
    })


# =========================
# USERS ANALYTICS
# =========================
@admin_bp.route("/analytics/users", methods=["GET"])
@jwt_required()
@admin_required
def user_analytics():

    total = User.query.count()

    admins = User.query.filter_by(role="admin").count()

    normal = User.query.filter_by(role="user").count()

    return jsonify({
        "total_users": total,
        "admins": admins,
        "users": normal
    })


# =========================
# MESSAGE ANALYTICS
# =========================
@admin_bp.route("/analytics/messages", methods=["GET"])
@jwt_required()
@admin_required
def message_analytics():

    total_messages = Message.query.count()

    reported_messages = Message.query.filter_by(
        is_reported=True
    ).count()

    return jsonify({
        "total_messages": total_messages,
        "reported_messages": reported_messages
    })


# =========================
# DELETE MESSAGE
# =========================
@admin_bp.route("/message/<int:msg_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_message(msg_id):

    msg = Message.query.get(msg_id)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(msg)
    db.session.commit()

    return jsonify({"message": "Message deleted"})