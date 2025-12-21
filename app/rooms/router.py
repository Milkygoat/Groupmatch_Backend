from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from .model import Room
from app.matchmaking.models import RoomMember
from .schemas import RoomResponse



router = APIRouter(prefix="/rooms", tags=["Rooms"])


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


@router.get("/my", response_model=RoomResponse)
def get_my_room(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    member = db.query(RoomMember).filter(
        RoomMember.user_id == user.id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="No active room")

    return db.query(Room).filter(Room.id == member.room_id).first()


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return room