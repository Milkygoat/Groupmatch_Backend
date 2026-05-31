from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProfileCreate(BaseModel):
    username: str
    name: str
    birthdate: date
    role: str
    skill: str
    pict: Optional[str] = None  


class ProfileOut(BaseModel):
    id: int
    user_id: int
    username: Optional[str] = None
    name: str
    birthdate: date
    role: str
    skill: str
    pict: Optional[str]

    class Config:
        from_attributes = True
