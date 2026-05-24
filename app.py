from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )