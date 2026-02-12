############## SETTINGS (DB_URL, SECRET_KEY, etc.) ##############

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "INHMP"
    DEBUG: bool = True
    DATABASE_URL: str = "mysql+pymysql://root:Password123!@localhost:3306/inhmp"
    SECRET_KEY: str = "hackathon-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    OTP_EXPIRE_SECONDS: int = 300

    class Config:
        env_file = ".env"

settings = Settings()