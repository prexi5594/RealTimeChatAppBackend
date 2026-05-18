from db import db
from datetime import datetime, timezone

class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    creator = db.relationship('User', backref='rooms')

    def __repr__(self):
        return f"<Room {self.room_name}>"