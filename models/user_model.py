<<<<<<< HEAD
from db import db
from datetime import datetime
=======
from extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
>>>>>>> 422b5bc (final changes)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD

    username = db.Column(db.String(80), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
=======
    username = db.Column(db.String(80), unique=True, nullable=False)

    # store hashed password here
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    is_online = db.Column(db.Boolean, default=False)
>>>>>>> 422b5bc (final changes)

    password = db.Column(db.String(255), nullable=False)

<<<<<<< HEAD
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
=======
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
>>>>>>> 422b5bc (final changes)

    def __repr__(self):
        return f"<User {self.username}>"
    