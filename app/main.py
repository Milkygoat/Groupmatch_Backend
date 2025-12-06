from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.auth.router import router as auth_router
from app.profile.router import router as profile_router
import cloudinary
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

models.User.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(profile_router)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Backend Group Match API Running"}
