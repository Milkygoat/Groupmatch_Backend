from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from .model import Room
from app.matchmaking.models import RoomMember
from .schemas import RoomResponse, RoomDetailResponse, RoomMemberDetail



router = APIRouter(prefix="/rooms", tags=["Rooms"])


def format_room_response(room: Room, db: Session) -> dict:
    """Convert room object to response with member details including role_id"""
    try:
        room_members = db.query(RoomMember).filter(RoomMember.room_id == room.id).all()
        
        members_list = []
        for room_member in room_members:
            try:
                user = room_member.user
                if not user:
                    continue
                    
                profile = user.profile
                members_list.append({
                    "user_id": user.id,
                    "name": profile.name if profile else "",
                    "username": user.username,
                    "role": room_member.role or (profile.role if profile else ""),
                    "role_id": room_member.role_id,
                    "pict": profile.pict if profile else None
                })
            except Exception as e:
                print(f"[ERROR] Error processing room_member {room_member.id}: {str(e)}")
                continue
        
        return {
            "id": room.id,
            "leader_id": room.leader_id,
            "status": room.status,
            "capacity": room.capacity,
            "current_count": room.current_count,
            "created_at": room.created_at,
            "members": members_list
        }
    except Exception as e:
        print(f"[ERROR] Error in format_room_response for room {room.id}: {str(e)}")
        # Fallback response
        return {
            "id": room.id,
            "leader_id": room.leader_id,
            "status": room.status,
            "capacity": room.capacity,
            "current_count": room.current_count,
            "created_at": room.created_at,
            "members": []
        }


# # GET /rooms - lihat semua room
# @router.get("/")
# def get_all_rooms(db: Session = Depends(get_db)):
#     return db.query(Room).all()



# # GET /rooms/my - lihat room user yang aktif
# @router.get("/my")
# def get_my_room(
#     db: Session = Depends(get_db),
#     user = Depends(get_current_user)
# ):
#     room = db.query(Room).filter(
#         Room.leader_id == user.id
#     ).first()

#     if not room:
#         return {"message": "Kamu belum ditempatkan dalam room."}

#     return room


@router.get("/")
def get_all_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@router.get("/my")
def get_my_room(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    member = db.query(RoomMember).filter(
        RoomMember.user_id == user.id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="No active room")

    room = db.query(Room).filter(Room.id == member.room_id).first()
    return format_room_response(room, db)


@router.get("/{room_id}")
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return format_room_response(room, db)


@router.post("/{room_id}/close")
def close_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Close room session - only leader can do this"""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Only leader can close room
    if room.leader_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only leader can close room")
    
    # Update room status to closed
    room.status = "closed"
    db.commit()
    
    # Add room history entries for closing
    from app.matchmaking.models import RoomHistory
    from datetime import datetime
    
    room_members = db.query(RoomMember).filter(RoomMember.room_id == room.id).all()
    for member in room_members:
        room_history = RoomHistory(
            room_id=room.id,
            user_id=member.user_id,
            action="closed",
            timestamp=datetime.now()
        )
        db.add(room_history)
    
    db.commit()
    return {"message": "Room closed successfully", "room_id": room.id}


@router.post("/{room_id}/leave")
def leave_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Leave room - any user can do this"""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Find and delete room member
    member = db.query(RoomMember).filter(
        RoomMember.room_id == room_id,
        RoomMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="User not in this room")
    
    # Add room history entry
    from app.matchmaking.models import RoomHistory
    from datetime import datetime
    
    room_history = RoomHistory(
        room_id=room.id,
        user_id=current_user.id,
        action="leave",
        timestamp=datetime.now()
    )
    db.add(room_history)
    
    # Delete from room_members
    db.delete(member)
    
    # Update room current_count
    room.current_count = max(0, room.current_count - 1)
    
    db.commit()
    return {"message": "Left room successfully", "room_id": room.id}