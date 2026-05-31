from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.rooms.model import Room
from app.db.models import Profile

from app.matchmaking.models import RoomHistory
from app.rooms.service import log_room_history


from .queue import (
    add_to_queue,
    is_in_queue,
    get_all_queue,
    remove_many_from_queue
)
from .models import RoomMember


# ROLE CONFIG
REQUIRED = {
    "qa": 1,
    "be": 1,
    "fe": 1,
    "pm": 1
}

ROLE_MAP = {
    "qa": "qa", "tester": "qa", "quality assurance": "qa",
    "be": "be", "backend": "be", "backend engineer": "be", "be engineer": "be",
    "fe": "fe", "frontend": "fe", "frontend engineer": "fe", "fe engineer": "fe",
    "pm": "pm", "project manager": "pm"
}

def normalize_role(raw: str) -> str:
    return ROLE_MAP.get(raw.lower(), raw.lower())


# JOIN MATCHMAKING
def join_matchmaking(db: Session, user_id: int, role: str):

    # cek sudah punya room?
    existing = db.query(RoomMember).filter(
        RoomMember.user_id == user_id
    ).first()

    if existing:
        return format_room_response(existing.room, "Already in room")

    # normalize role
    normalized = normalize_role(role)

    # cek queue
    if is_in_queue(db, user_id):
        return {"status": "waiting", "message": "Already in queue"}

    # add ke queue
    add_to_queue(db, user_id, normalized)

    # proses matchmaking
    room = try_process_match(db)
    if room:
        return room

    return {"status": "waiting", "message": "Joined matchmaking queue"}



# MATCHMAKING CORE - Membutuhkan 4 role (BE, FE, QA, PM)
def try_process_match(db: Session):
    queue = get_all_queue(db)

    # Group queue by role
    role_buckets = {}
    for q in queue:
        role_buckets.setdefault(q.role, []).append(q)

    # Cek apakah semua 4 role tersedia
    for role, count in REQUIRED.items():
        if len(role_buckets.get(role, [])) < count:
            return None  # belum cukup, tetap waiting

    # Ambil 1 user dari setiap role (4 orang total)
    selected = []
    for role, count in REQUIRED.items():
        selected.extend(role_buckets[role][:count])

    user_ids = [q.user_id for q in selected]

    room = Room(
        status="active",
        capacity=4,
        current_count=4,
        leader_id=user_ids[0]
    )
    db.add(room)
    db.commit()
    db.refresh(room)

    for q in selected:
        profile = db.query(Profile).filter(
            Profile.user_id == q.user_id
        ).first()

        member = RoomMember(
            room_id=room.id,
            user_id=q.user_id,
            role=profile.role if profile else q.role
        )
        db.add(member)

        # 🔥 LOG JOIN
        log_room_history(
            db=db,
            room_id=room.id,
            user_id=q.user_id,
            action="join"
        )

    db.commit()

    remove_many_from_queue(db, user_ids)

    return {
        "status": "matched",
        "message": "Matched",
        "room_id": room.id,
        "leader_id": room.leader_id
    }





# END ROOM
def end_room(db: Session, leader_id: int):
    room = db.query(Room).filter(
        Room.leader_id == leader_id,
        Room.status == "active"
    ).first()

    if not room:
        raise HTTPException(status_code=400, detail="Leader has no room")

    room.status = "closed"
    room.leader_id = None

    db.query(RoomMember).filter(
        RoomMember.room_id == room.id
    ).delete()

    log_room_history(
        db=db,
        room_id=room.id,
        user_id=leader_id,
        action="closed"
    )

    db.commit()

    return {"message": "Room ended", "room_id": room.id}




# RESPONSE FORMAT
def format_room_response(room: Room, message: str):
    return {
        "status": "matched",
        "message": message,
        "room_id": room.id,
        "leader_id": room.leader_id,
        "members": [
            {"user_id": m.user_id}
            for m in room.members
        ]
    }

def log_room_history(db: Session, room_id: int, user_id: int, action: str):
    history = RoomHistory(
        room_id=room_id,
        user_id=user_id,
        action=action,
        timestamp=datetime.utcnow()
    )
    db.add(history)
    db.commit()
