from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class MemberInfo(BaseModel):
    user_id: int
    name: str
    username: str
    role: str
    pict: Optional[str] = None

    class Config:
        from_attributes = True


class RoomResponse(BaseModel):
    id: int
    leader_id: int | None
    status: str
    capacity: int
    current_count: int
    created_at: datetime
    members: List[MemberInfo] = []

    class Config:
        from_attributes = True
