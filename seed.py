from app import app, db
from models.room_model import Room

# Define the rooms your React frontend is looking for
rooms_to_create = [
    {"id": 2, "name": "Sports", "topic": "Sports & Athletics", "description": "Discuss football, basketball, tennis, and more!"},
    {"id": 3, "name": "Politics", "topic": "Politics & Government", "description": "Political discussions and debates"},
    {"id": 4, "name": "Fashion", "topic": "Fashion & Style", "description": "Latest trends, tips, and fashion advice"}
]

with app.app_context():
    for room_data in rooms_to_create:
        if not Room.query.get(room_data["id"]):
            new_room = Room(**room_data)
            db.session.add(new_room)
            print(f"Added room: {room_data['name']} (ID: {room_data['id']})")
        else:
            print(f"Room {room_data['name']} (ID: {room_data['id']}) already exists.")
    db.session.commit()
    print("Database seeding finished.")