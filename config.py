import os
class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-fallback-jwt-key-67890")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///chat.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
