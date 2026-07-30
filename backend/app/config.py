from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ==============================
    # DATABASE & SECURITY
    # ==============================
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # ==============================
    # APPLICATION
    # ==============================
    ENVIRONMENT: str = "development"
    APP_NAME: str = "METHYLOX™ Global Enterprise SaMD Engine"
    APP_VERSION: str = "3.0.0"

    # ==============================
    # SMTP (OPTIONAL)
    # ==============================
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    CLINICAL_ALERT_EMAIL: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
