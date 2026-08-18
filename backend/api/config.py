from functools import lru_cache
from os import getenv
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = getenv("DATABASE_URL")
    SECRET_KEY: str = getenv("SECRET_KEY")
    ALGORITHM: str = getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60 * 24)  # 1 day
    CORS_ORIGINS: list[str] = __import__("json").loads(getenv("CORS_ORIGINS") or '["http://localhost:5173"]')
    GOOGLE_SERVICE_ACCOUNT_JSON: str = getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    GOOGLE_SHEETS_SPREADSHEET_ID: str = getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Module-level settings instance for convenient imports
settings = get_settings()