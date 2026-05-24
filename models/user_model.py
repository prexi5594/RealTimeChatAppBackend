from datetime import datetime, timezone

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # =====================
    # USER STATUS FIELDS
    # =====================
    role = db.Column(
        db.String(20),
        default="user"
    )

    is_banned = db.Column(
        db.Boolean,
        default=False
    )

    is_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_online = db.Column(
        db.Boolean,
        default=False
    )

    # =====================
    # OTP FIELDS (ADD THIS HERE)
    # =====================
    otp_code = db.Column(
        db.String(6),
        nullable=True
    )

    otp_verified = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # =====================
    # PASSWORD HELPERS
    # =====================
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # =====================
    # SERIALIZER
    # =====================
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_verified": self.is_verified,
            "otp_verified": self.otp_verified,
            "is_online": self.is_online,
            "is_banned": self.is_banned,
            "created_at": self.created_at.isoformat()
        }