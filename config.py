import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # =========================
    # SECURITY
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # =========================
    # DATABASE
    # =========================
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///local.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # CORS
    # =========================
    CORS_ORIGINS = [
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://realtimechatapp2-vgnu.onrender.com"
    ]

    # =========================
    # SENDGRID EMAIL (IMPORTANT)
    # =========================
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    MAIL_FROM = os.getenv("MAIL_FROM")