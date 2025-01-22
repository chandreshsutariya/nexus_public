import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    UPLOAD_FOLDER = 'data/temp'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit upload size to 16MB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
