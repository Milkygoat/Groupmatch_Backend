from pydantic import BaseModel

class JoinMatchmakingRequest(BaseModel):
    user_id: int
    role: str  # optional: tank, fighter, support, etc.

class JoinMatchmakingResponse(BaseModel):
    message: str
