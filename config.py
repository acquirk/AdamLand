import os

class Config:
    SECRET_KEY = '4b2e2f12ff1e9c33a69f9fbd1f63b2a1'  # You should use a strong, random key in production
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/adamland'
    SQLALCHEMY_TRACK_MODIFICATIONS = False