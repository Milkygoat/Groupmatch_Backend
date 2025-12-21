from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    room_id: int
    message: str


class MessageResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    username: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class RoomChatHistory(BaseModel):
    room_id: int
    messages: list[MessageResponse] = []
