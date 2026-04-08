import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "kanak-secret-key-2026")
    _db_url = os.getenv("DATABASE_URL")
    if _db_url:
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        db_user = os.getenv("DB_USER", "root")
        db_password = quote_plus(os.getenv("DB_PASSWORD", "Kanak#456"))
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_port = os.getenv("DB_PORT", "3307")
        db_name = os.getenv("DB_NAME", "institutional_tracker_live")
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "xlsx", "xls", "docx"}

    DEMO_USERS = {
        "admin@institution.edu": {
            "password": "admin123",
            "role": "admin",
            "name": "Aarav Sharma",
        },
        "teacher@institution.edu": {
            "password": "teacher123",
            "role": "teacher",
            "name": "Dr. Meera Singh",
        },
        "student@institution.edu": {
            "password": "student123",
            "role": "student",
            "name": "Riya Patel",
        },
    }
