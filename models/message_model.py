from extensions import db
from datetime import datetime, timezone

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(80), nullable=False)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    is_deleted = db.Column(db.Boolean, default=False)
    is_reported = db.Column(db.Boolean, default=False)

    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )