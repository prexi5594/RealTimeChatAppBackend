from extensions import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(100), nullable=False)

    # THIS IS WHAT YOU WERE MISSING / BROKEN
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.message}>"