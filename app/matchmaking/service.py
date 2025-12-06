from sqlalchemy.orm import Session
from fastapi import HTTPException
import random
from .models import Room, RoomMember, RoomHistory
from .queue import add_to_queue, count_queue, get_all_queue, clear_queue
from app.db.models import Profile  # kalau file kamu beda, sesuaikan

TEAM_SIZE = 5  # jumlah anggota untuk buat room

def join_matchmaking(db: Session, user_id: int, role: str):
    # 1. cek user punya profile
    profile = db.query(Profile).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="User belum membuat profile.")

    # 2. cek user sudah dalam queue
    #    kita pakai helper
    from .queue import is_in_queue
    if is_in_queue(db, user_id):
        raise HTTPException(status_code=400, detail="User sudah berada dalam queue.")

    # 3. masukkan ke queue
    add_to_queue(db, user_id, role)

    # 4. cek queue penuh?
    if count_queue(db) >= TEAM_SIZE:
        return create_room(db)

    return {"message": "Joined matchmaking queue"}

def create_room(db: Session):
    # ambil semua user di queue
    queue_users = get_all_queue(db)
    user_ids = [u.user_id for u in queue_users]

    # pilih leader random
    leader_id = random.choice(user_ids)

    # buat room baru
    room = Room(leader_id=leader_id)
    db.add(room)
    db.commit()
    db.refresh(room)

    # masukkan semua member
    for user_id in user_ids:
        member = RoomMember(room_id=room.id, user_id=user_id)
        db.add(member)

        # tambah history
        history = RoomHistory(room_id=room.id, user_id=user_id, action="join")
        db.add(history)

    db.commit()

    # bersihkan queue
    clear_queue(db)

    return {
        "message": "Room created",
        "room_id": room.id,
        "leader_id": leader_id
    }
