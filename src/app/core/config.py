# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from .jwt_manager import JWTManager
import logging


# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DATABASE_URL_SYNC: str = Field(..., env="DATABASE_URL_SYNC")

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ISSUER: str = "mantadive"
    AUDIENCE: str = "diver-users"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()


# Initialize JWTManager
jwt_manager = JWTManager(secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)