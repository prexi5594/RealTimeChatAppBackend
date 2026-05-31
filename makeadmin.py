from app import app, db
from models.user_model import User

with app.app_context():
    user = User.query.filter_by(email="zayda@mtkenyaacademy.ac.ke").first()

    if user:
        user.role = "admin"
        db.session.commit()
        print("SUCCESS: User is now admin")
    else:
        print("User not found")