import os

class Config:
    SECRET_KEY = 'abc'

    DEBUG = True

    # Connect to the database
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abc@localhost:5432/fyyur'

    # Optional: turn off warnings for development 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


    # Edited: Config class