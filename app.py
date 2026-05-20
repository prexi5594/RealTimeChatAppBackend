from flask import Flask
from flask_cors import CORS
from extensions import db

def create_app():
    app = Flask(__name__)

    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

   
    db.init_app(app)
    CORS(app)

    # IMPORT + REGISTER BLUEPRINTS
    from routes.auth_routes import auth_bp
    from routes.room_routes import room_bp
    from routes.message_routes import message_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(message_bp)

    
    @app.route("/")
    def home():
        return {"message": "HEY CHAT"}

    return app


app = create_app()

from models.room_model import Room 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

       
        if not Room.query.first():
            db.session.add(Room(name="Sports"))
            db.session.add(Room(name="Politics"))
            db.session.add(Room(name="Fashion"))
            db.session.commit()

    app.run(debug=True, host="0.0.0.0", port=5000)