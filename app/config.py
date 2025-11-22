from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "LogPages API"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OTP
    OTP_EXPIRE_MINUTES: int = 5
    OTP_LENGTH: int = 6

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    USE_REDIS: bool = False

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Keycloak
    KEYCLOAK_REALM: str = "myrealm"
    KEYCLOAK_BASE_URL: str = "http://localhost:8080"
    KEYCLOAK_CLIENT_ID: str = "app-backend"
    KEYCLOAK_CLIENT_SECRET: str = "change-me"
    KEYCLOAK_DUMMY_PASSWORD: str = "dummy-password"

    # Email (Gmail SMTP)
    SMTP_EMAIL: str = ""  # Ton email Gmail
    SMTP_PASSWORD: str = ""  # App Password Gmail (16 caractères sans espaces)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
