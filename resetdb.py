from app import app, db
from models.room_model import Room
from models.message_model import Message

with app.app_context():

    # 1. Delete messages first (IMPORTANT because of foreign key)
    db.session.query(Message).delete()

    # 2. Delete rooms
    db.session.query(Room).delete()

    db.session.commit()

    # 3. Reset auto-increment sequence (PostgreSQL)
    db.session.execute(db.text("ALTER SEQUENCE rooms_id_seq RESTART WITH 1"))
    db.session.execute(db.text("ALTER SEQUENCE messages_id_seq RESTART WITH 1"))

    db.session.commit()

    print(" Database fully reset (rooms + messages + sequences)")