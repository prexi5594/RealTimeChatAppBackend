
from flask import Flask
from flask_cors import CORS
def create_app():
    app = Flask(__name__)

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
    app.run(debug=True)