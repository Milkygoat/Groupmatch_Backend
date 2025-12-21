from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user
from app.chat.service import save_message, get_chat_history, format_message_response
from app.chat.schemas import MessageCreate, MessageResponse, RoomChatHistory

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/{room_id}/history", response_model=RoomChatHistory)
def get_room_chat_history(
    room_id: int,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for a room"""
    try:
        messages = get_chat_history(db, room_id, limit)
        formatted_messages = [
            format_message_response(msg, db) for msg in messages
        ]
        
        return {
            "room_id": room_id,
            "messages": formatted_messages,
            "total_messages": len(formatted_messages)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[CHAT] Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{room_id}/message", response_model=MessageResponse)
def send_message(
    room_id: int,
    message_data: MessageCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to room chat"""
    try:
        # Extract user_id from current_user
        user_id = current_user.id
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        # Save message
        message = save_message(db, room_id, user_id, message_data.message)
        
        # Format response
        response = format_message_response(message, db)
        return MessageResponse(**response)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[CHAT] Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
