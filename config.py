import os
from datetime import timedelta

class Config:
    # Use a safe fallback string for local development if environment variables are missing
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-secret-key-12345")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-fallback-jwt-key-67890")
    
    # SQLite fallback for local development; Render should inject a real PostgreSQL URL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///chat.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Mail configurations (Safe defaults)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")