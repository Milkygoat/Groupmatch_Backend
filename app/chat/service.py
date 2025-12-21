from sqlalchemy.orm import Session
from app.db.models import RoomMessage, User
from app.rooms.model import Room
from fastapi import HTTPException
from datetime import datetime


def save_message(db: Session, room_id: int, user_id: int, message: str) -> RoomMessage:
    """Save message to database"""
    # Verify room exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Verify user is in room
    from app.matchmaking.models import RoomMember
    member = db.query(RoomMember).filter(
        RoomMember.room_id == room_id,
        RoomMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="User not in this room")
    
    # Create and save message
    db_message = RoomMessage(
        room_id=room_id,
        user_id=user_id,
        message=message,
        created_at=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message


def get_chat_history(db: Session, room_id: int, limit: int = 100) -> list[RoomMessage]:
    """Get chat history for a room"""
    # Verify room exists
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Get messages sorted by created_at
    messages = db.query(RoomMessage).filter(
        RoomMessage.room_id == room_id
    ).order_by(RoomMessage.created_at.asc()).limit(limit).all()
    
    return messages


def format_message_response(message: RoomMessage, db: Session) -> dict:
    """Format message for API response"""
    user = db.query(User).filter(User.id == message.user_id).first()
    
    return {
        "id": message.id,
        "room_id": message.room_id,
        "user_id": message.user_id,
        "username": user.username if user else "Unknown",
        "message": message.message,
        "created_at": message.created_at.isoformat() if message.created_at else None
    }
