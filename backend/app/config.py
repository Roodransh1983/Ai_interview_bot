"""
Application settings — loaded from environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ai_interview_bot"

    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Interview Settings
    QUESTIONS_PER_INTERVIEW: int = 5
    QUESTION_TIME_SECONDS: int = 120  # 2 minutes per question

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
