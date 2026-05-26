import os


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "dev-fallback-jwt-key-67890"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False