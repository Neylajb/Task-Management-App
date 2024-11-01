import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://taskmanager:taskmanager@127.0.0.1:5432/taskmanager")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
