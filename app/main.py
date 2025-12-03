from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.auth.router import router as auth_router

models.User.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Backend Group Match API Running"}
