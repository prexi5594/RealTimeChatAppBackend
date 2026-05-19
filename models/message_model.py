from db import db
from datetime import datetime, timezone

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='messages', overlaps="messages")
    room = db.relationship('Room', backref='messages')

    def __repr__(self):
        return f"<Message {self.id} by User {self.user_id}>"
    
    