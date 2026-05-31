from app import app
from extensions import db
from models.room_model import Room

rooms_to_create = [
    {
        "id": 1,
        "name": "General",
        "topic": "Welcome",
        "description": "Default room"
    },
    {
        "id": 2,
        "name": "Sports",
        "topic": "Sports & Athletics",
        "description": "Discuss football, basketball, tennis, and more!"
    },
    {
        "id": 3,
        "name": "Politics",
        "topic": "Politics & Government",
        "description": "Political discussions and debates"
    },
    {
        "id": 4,
        "name": "Fashion",
        "topic": "Fashion & Style",
        "description": "Latest trends, tips, and fashion advice"
    }
]

with app.app_context():
    for room_data in rooms_to_create:
        existing = Room.query.get(room_data["id"])

        if not existing:
            room = Room(**room_data)
            db.session.add(room)
            print(f"Added {room.name}")
        else:
            print(f"{existing.name} already exists")

    db.session.commit()

print("Database seeding finished.")