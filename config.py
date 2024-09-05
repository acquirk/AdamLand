import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4b2e2f12ff1e9c33a69f9fbd1f63b2a1'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f"Database URL: {SQLALCHEMY_DATABASE_URI}")  # Temporary debug print
