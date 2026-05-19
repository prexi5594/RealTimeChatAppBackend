import os

class Config:
    db_url = os.environ.get("DATABASE_URL")

    SQLALCHEMY_DATABASE_URI = (
        db_url.replace("postgres://", "postgresql+psycopg2://")
        if db_url else None
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False