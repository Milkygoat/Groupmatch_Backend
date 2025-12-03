from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth import schemas, service
from app.auth.google_oauth import generate_google_login_url, get_google_user
from app.auth.github_oauth import (
    generate_github_login_url,
    get_github_access_token,
    get_github_user
)
from app.core.security import create_access_token
from app.db import models

router = APIRouter(prefix="/auth", tags=["Auth"])


# ============================
# Register
# ============================
@router.post("/register")
def register(data: schemas.RegisterRequest, db: Session = Depends(get_db)):
    user = service.register_user(data, db)
    return {"message": "Register success", "user": user}


# ============================
# Login
# ============================
@router.post("/login")
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    token, user = service.login_user(data, db)

    return {
        "message": "Login success",
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }


# ============================
# Google OAuth: Login URL
# ============================
@router.get("/google/login")
def google_login():
    return {"login_url": generate_google_login_url()}





# ============================
# Google OAuth Callback
# ============================
@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    # Ambil user dari Google
    google_user = await get_google_user(code)

    email = google_user["email"]
    name = google_user.get("name", "")
    picture = google_user.get("picture", "")

    # Cek apakah user sudah ada
    existing_user = db.query(models.User).filter(models.User.email == email).first()

    if not existing_user:
        username = email.split("@")[0]

        new_user = models.User(
            name=name,
            email=email,
            username=username,
            password="oauth",       # dummy password, tidak dipakai
        )

        # kalau mau simpan pict, tambahkan kolom dulu di model
        # new_user.pict = picture

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user = new_user
    else:
        user = existing_user

    # Buat JWT Token
    token = create_access_token({"sub": user.email})

    return {
        "message": "Login via Google success",
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "username": user.username,
        }
    }

# ============================
# GitHub OAuth: Login URL
# ============================
@router.get("/github/login")
def github_login():
    return {"login_url": generate_github_login_url()}


# ============================
# GitHub OAuth Callback
# ============================
@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    # Step 1: Dapatkan access token dari GitHub
    access_token = await get_github_access_token(code)

    # Step 2: Dapatkan data user GitHub
    github_user = await get_github_user(access_token)

    email = github_user.get("email")
    username = github_user.get("login")
    name = github_user.get("name") or username
    avatar = github_user.get("avatar_url")

    if email is None:
        raise HTTPException(400, "Email GitHub tidak tersedia, aktifkan 'Email → Public email' di GitHub settings.")
