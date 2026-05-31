import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


# LOAD ENV (LOCAL / PROD)
ENV = os.getenv("ENV", "local")

if ENV == "production":
    load_dotenv(".env.railway")
else:
    load_dotenv(".env.local")


# DATABASE & MODELS
from app.db.database import Base, engine
from app.db import models
from app.rooms.model import Room
from app.matchmaking.models import RoomMember, MatchmakingQueue

Base.metadata.create_all(bind=engine)


# ROUTERS
from app.auth.router import router as auth_router
from app.profile.router import router as profile_router
from app.matchmaking.router import router as matchmaking_router
from app.rooms.router import router as room_router
from app.ws.router import router as ws_router


# CONFIG
import cloudinary
from app.core.config import settings


# APP
app = FastAPI(debug=True)


# CORS
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

if ENV == "production":
    allowed_origins.append("https://groupmatchuas-production.up.railway.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CLOUDINARY
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


# ROUTER REGISTER
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(matchmaking_router)
app.include_router(room_router)
app.include_router(ws_router)


# ROOT
@app.get("/")
def home():
    return {"message": "Backend Group Match API Running"}
