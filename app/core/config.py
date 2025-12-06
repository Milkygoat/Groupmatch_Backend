import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

# class Settings:
#     GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
#     GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
#     GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"

#     GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
#     GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
#     GITHUB_REDIRECT_URI = "http://localhost:8000/auth/github/callback"

class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_REDIRECT_URI: str

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"
        extra = "allow"  # optional, biar aman kalau ada var lain

settings = Settings()

