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

    CORS(app)
    
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.room_routes import room_bp
    from routes.message_routes import message_bp
    from routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(user_bp)

    
    with app.app_context():
        import models.user_model
        import models.room_model
        import models.message_model

        db.create_all()

    @app.route("/")
    def home():
        return {"message": "Backend running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)