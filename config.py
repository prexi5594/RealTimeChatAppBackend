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
    DATABASE_URL = fix_db_url(os.getenv("DATABASE_URL"))
    
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is missing!")
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
        
    if "sslmode" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL 
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