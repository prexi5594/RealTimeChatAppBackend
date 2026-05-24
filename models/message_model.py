from extensions import db
from datetime import datetime, timezone


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        nullable=False
    )

    # =========================
    # SOFT DELETE
    # =========================
    is_deleted = db.Column(
        db.Boolean,
        default=False
    )

    # =========================
    # REPORT SYSTEM
    # =========================
    is_reported = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )