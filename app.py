import os
from flask import Flask
from flask_cors import CORS
from config import Config
from db import db
from flask_jwt_extended import JWTManager
from flask_mail import Mail

jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Explicit CORS configuration targeting your Vite dev environment
    CORS(
        app,
        resources={r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ]
        }},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Blueprint imports
    from routes.auth_routes import auth_bp
    from routes.room_routes import room_bp
    from routes.message_routes import message_bp
    from routes.user_routes import user_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(user_bp)

    # Context-bound configurations (Database setup)
    with app.app_context():
        import models.user_model
        import models.room_model
        import models.message_model
        
        # Creates tables if they don't exist
        db.create_all()

    @app.route("/")
    def home():
        return {"status": "healthy", "message": "Backend running successfully"}

    return app  

app = create_app()

if __name__ == "__main__":
    # Render overrides port via environment variable; falls back to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)