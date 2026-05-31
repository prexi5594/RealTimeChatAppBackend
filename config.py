import os
from dotenv import load_dotenv

load_dotenv()

def fix_db_url(url):
    if not url:
        return None

    
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://")

   
    if "sslmode" not in url:
        url += "?sslmode=require"

    return url


class Config:

    # =========================
    # SECURITY
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # =========================
    # DATABASE
    # =========================
    raw_db = os.getenv("DATABASE_URL")

    if not raw_db:
        SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
    else:
        raw_db = raw_db.strip()

        if raw_db.startswith("postgres://"):
            raw_db = raw_db.replace("postgres://", "postgresql+psycopg2://", 1)

        if raw_db.startswith("postgresql://"):
            raw_db = raw_db.replace("postgresql://", "postgresql+psycopg2://", 1)

        SQLALCHEMY_DATABASE_URI = raw_db

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
    # EMAIL (SendGrid)
    # =========================
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    MAIL_FROM = os.getenv("MAIL_FROM")