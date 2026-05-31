import os
from dotenv import load_dotenv
import traceback
from flask_mail import Message

load_dotenv()


class Config:
    # =========================
    # CORE SECURITY
    # =========================
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "dev-jwt-secret"
    )

    # =========================
    # DATABASE
    # =========================
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:

        # Fix old postgres:// format
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://"
            )

        # FORCE SSL
        if "?sslmode=" not in DATABASE_URL:
            DATABASE_URL += "?sslmode=require"

    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL or "sqlite:///local.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # =========================
    # CORS
    # =========================
    CORS_ORIGINS = [
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://realtimechatapp2-vgnu.onrender.com"
    ]

    # =========================
    # MAIL CONFIG
    # =========================
    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587
    
    MAIL_USE_SSL = False

    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    
    MAIL_TIMEOUT = 5 