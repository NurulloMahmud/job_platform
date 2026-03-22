from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "Job Platform"
    DEBUG: bool = True
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/job_platform.db"

    SECRET_KEY: str = "89305262714c9cd5b94c58aae1b809217eec324df53fd4202509a1e37e3e9912"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
