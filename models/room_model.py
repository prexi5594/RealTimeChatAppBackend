from db import db

__tablename__ = "rooms"

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )