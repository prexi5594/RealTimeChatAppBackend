from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config


db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

   
    app.config.from_object(Config)

    
    CORS(app)

    
    db.init_app(app)

    
  
    from routes.auth_routes import auth_bp
    from routes.room_routes import room_bp
    from routes.message_routes import message_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(message_bp)

    
    with app.app_context():
        db.create_all()

    
    @app.route("/")
    def home():
        return {
            "message": "Backend is running successfully"
        }

    return app



app = create_app()



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )