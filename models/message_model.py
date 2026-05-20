from extensions import db
from datetime import datetime, timezone


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("rooms.id"),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship(
        "User",
        backref="messages",
        lazy=True
    )

    room = db.relationship(
        "Room",
        backref="messages",
        lazy=True
    )

    def __repr__(self):
        return f"<Message {self.id}>"