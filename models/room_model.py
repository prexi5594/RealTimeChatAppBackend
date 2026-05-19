from db import db



class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )