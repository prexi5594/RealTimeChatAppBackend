from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()  

from config import Config
from extensions import db, mail
from routes.auth_routes import auth_bp
from routes.room_routes import room_bp
from routes.message_routes import message_bp


# =========================
# APP SETUP
# =========================
app = Flask(__name__)
app.config.from_object(Config)

# =========================
# CORS
# =========================
CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost:5174",
        "https://realtimechatapp2-vgnu.onrender.com"
    ]}},
    supports_credentials=True,
    methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# =========================
# EXTENSIONS
# =========================
db.init_app(app)
jwt = JWTManager(app)
mail.init_app(app)

# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth_bp)
app.register_blueprint(room_bp)
app.register_blueprint(message_bp)

# =========================
# HEALTH CHECK
# =========================
@app.route("/")
def home():
    return jsonify({"message": "Backend running"}), 200


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)