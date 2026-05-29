from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

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
# CORS FIX (IMPORTANT)
# =========================
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
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
# BLUEPRINTS ONLY
# =========================
app.register_blueprint(auth_bp)
app.register_blueprint(room_bp)
app.register_blueprint(message_bp)


# =========================
# DB INIT
# =========================
with app.app_context():
    db.create_all()

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
    app.run(debug=True, port=5000)