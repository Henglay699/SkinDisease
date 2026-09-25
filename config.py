import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    
    # Store the key variable here
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(INSTANCE_DIR, "skindisease.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False