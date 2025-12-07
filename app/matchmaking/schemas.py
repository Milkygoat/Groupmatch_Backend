# from pydantic import BaseModel

# class JoinMatchmakingRequest(BaseModel):
#     user_id: int
#     role: str  # optional: tank, fighter, support, etc.

# class JoinMatchmakingResponse(BaseModel):
#     message: str

from pydantic import BaseModel
from typing import Optional

class JoinMatchmakingResponse(BaseModel):
    message: str
    room_id: Optional[int] = None
    leader_id: Optional[int] = None
