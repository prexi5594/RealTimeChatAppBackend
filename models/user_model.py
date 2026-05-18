from db import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    password_hash = db.Column(
        db.String(300),
        nullable=False
    )

    # when user account is created
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # optional but useful for chat apps
    is_online = db.Column(db.Boolean, default=False)

    last_seen = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"