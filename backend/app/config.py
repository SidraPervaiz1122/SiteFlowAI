import os
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "SiteFlow AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Storage & DB
    STORAGE_DIR: str = str(BASE_DIR / "storage")
    UPLOADS_DIR: str = str(BASE_DIR / "storage" / "uploads")
    DOCUMENTS_DIR: str = str(BASE_DIR / "storage" / "documents")
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/storage/siteflow.db"
    
    # Auth
    SECRET_KEY: str = "siteflow-super-secret-key-for-jwt-signing-2026-production-ready"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # AI Configuration
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    AI_PROVIDER: str = "mock" # "mock" | "openai" | "gemini"
    AI_FALLBACK_ENABLED: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
