from flask import Flask
from flask_cors import CORS
from config import Config
from db import db


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Enable CORS (for frontend communication)
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Import and register blueprints (routes)
    from routes.auth_routes import auth_bp
    from routes.room_routes import room_bp
    from routes.message_routes import message_bp
    from routes.user_routes import user_bp  # if you have it

    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(user_bp)

    # Home route (test server)
    @app.route("/")
    def home():
        return {"message": "Backend is running successfully"}

    # Create database tables
    with app.app_context():
        # IMPORTANT: import models before create_all()
        from models.user_model import User
        from models.room_model import Room
        from models.message_model import Message

        db.create_all()

    return app


# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )