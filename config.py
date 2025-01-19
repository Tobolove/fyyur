import os
SECRET_KEY = 'abc'


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abc@localhost:5432/fyyur'

# Optional: Silence deprecation warnings
SQLALCHEMY_TRACK_MODIFICATIONS = False