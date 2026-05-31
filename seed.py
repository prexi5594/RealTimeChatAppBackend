from app import app, db
from models.room_model import Room

rooms = [
    {"name": "General", "topic": "Welcome", "description": "Default chat room"},
    {"name": "Sports", "topic": "Sports & Athletics", "description": "Discuss football, basketball, tennis, and more!"},
    {"name": "Politics", "topic": "Politics & Government", "description": "Political discussions and debates"},
    {"name": "Fashion", "topic": "Fashion & Style", "description": "Latest trends and style talk"},
]

with app.app_context():
    for r in rooms:
        exists = Room.query.filter_by(name=r["name"]).first()

        if not exists:
            room = Room(
                name=r["name"],
                topic=r["topic"],
                description=r["description"]
            )
            db.session.add(room)
            print(f"Added: {r['name']}")
        else:
            print(f"Already exists: {r['name']}")

    db.session.commit()
    print(" Seeding complete")