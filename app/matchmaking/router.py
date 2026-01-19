from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user   # ✅ SATU INI SAJA
from app.matchmaking.service import join_matchmaking, end_room
from app.matchmaking.models import RoomMember, MatchmakingQueue
from app.db.models import Profile
from app.matchmaking.service import log_room_history

router = APIRouter(prefix="/matchmaking", tags=["Matchmaking"])


def get_room_members(db: Session, room_id: int):
    members = db.query(RoomMember).filter(
        RoomMember.room_id == room_id
    ).all()

    return [
        {
            "user_id": m.user_id,
            "role": m.role
        }
        for m in members
    ]


@router.post("/join")
def join_queue(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # pastikan user punya profile
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=400,
            detail="User belum membuat profile"
        )

    # jika sudah punya room → BALIKIN ROOM ITU
    existing = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id
    ).first()

    if existing:
        room = existing.room
        return {
            "status": "matched",
            "message": "User already in a room",
            "room_id": room.id,
            "leader_id": room.leader_id,
            "members": get_room_members(db, room.id)
        }

    # matchmaking
    return join_matchmaking(
        db=db,
        user_id=current_user.id,
        role=profile.role
    )


@router.get("/status")
def matchmaking_status(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    member = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id
    ).first()

    if member:
        room = member.room
        return {
            "status": "matched",
            "room_id": room.id,
            "leader_id": room.leader_id,
            "members": get_room_members(db, room.id)
        }

    in_queue = db.query(MatchmakingQueue).filter(
        MatchmakingQueue.user_id == current_user.id
    ).first()

    if in_queue:
        return {"status": "waiting"}

    return {"status": "idle"}


@router.post("/end-room")
def end_room_endpoint(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return end_room(
        db=db,
        leader_id=current_user.id
    )

@router.post("/leave")
def leave_room(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    member = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="User not in room")

    room_id = member.room_id

    db.delete(member)
    db.commit()

    log_room_history(
        db=db,
        room_id=room_id,
        user_id=current_user.id,
        action="leave"
    )

    return {"message": "Left room"}

