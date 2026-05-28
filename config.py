import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-fallback-jwt-key-67890")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://chat_db_v2_user:O5keeC9K8Qp0ASqy42zFRbDUMytXEuiM@dpg-d86cibm7r5hc739ssilg-a/chat_db_v2"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MAIL CONFIG (YOU WERE MISSING THESE)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")