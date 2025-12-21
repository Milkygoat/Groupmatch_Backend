from sqlalchemy.orm import Session
from fastapi import HTTPException
import random
from app.rooms.model import Room
from .queue import (
    add_to_queue,
    is_in_queue,
    get_all_queue,
    get_queue_by_role,
    remove_many_from_queue
)
from app.db.models import Profile

# roles required (normalized keys)
REQUIRED = {
    "qa": 1,
    "be": 1,
    "fe": 1
}

# map possible role strings to normalized keys
ROLE_MAP = {
    "project manager": "pm",
    "project_manager": "pm",
    "pm": "pm",

    "quality assurance": "qa",
    "quality_assurance": "qa",
    "qa": "qa",
    "tester": "qa",
    "quality": "qa",

    "backend": "be",
    "back-end": "be",
    "be": "be",
    "backend dev": "be",
    "backend_dev": "be",

    "frontend": "fe",
    "front-end": "fe",
    "fe": "fe",
    "frontend dev": "fe",
    "frontend_dev": "fe",
}

def normalize_role(raw: str) -> str:
    if not raw:
        return raw
    r = raw.strip().lower().replace("-", " ").replace(".", " ")
    # try direct match first
    if r in ROLE_MAP:
        return ROLE_MAP[r]
    # try word contains
    for k in ROLE_MAP:
        if k in r:
            return ROLE_MAP[k]
    # fallback: if single word 'backend' etc
    token = r.split()[0]
    return ROLE_MAP.get(token, r)  # if can't map, return original (unsafe)

def join_matchmaking(db: Session, user_id: int, role: str):
    try:
        print(f"\n[MATCHMAKING] =================================================================")
        print(f"[MATCHMAKING] USER {user_id} JOINING MATCHMAKING")
        print(f"[MATCHMAKING] =================================================================")
        
        # 0. cek apakah user sudah ada di room
        from app.matchmaking.models import RoomMember
        existing_member = db.query(RoomMember).filter(
            RoomMember.user_id == user_id
        ).first()
        
        if existing_member:
            print(f"[MATCHMAKING] ⚠️ User already in room {existing_member.room_id}")
            return {
                "message": "Already in room",
                "room_id": existing_member.room_id
            }
        
        # 1. cek profile ada
        profile = db.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            raise HTTPException(status_code=400, detail="User belum membuat profile.")

        # normalize role from profile if role param not passed
        normalized = normalize_role(role or profile.role)
        print(f"[MATCHMAKING] Original role: '{role or profile.role}' → Normalized: '{normalized}'")

        # 2. cek sudah di queue?
        if is_in_queue(db, user_id):
            print(f"[MATCHMAKING] ⚠️ User already in queue, returning waiting status")
            return {"message": "Already in queue"}

        # 3. tambah ke queue
        add_to_queue(db, user_id, normalized)
        print(f"[MATCHMAKING] ✅ User added to queue")

        # 4. coba proses matchmaking
        created = try_process_match(db)
        
        if created:
            print(f"[MATCHMAKING] ✅ ROOM CREATED! Room ID: {created['room_id']}")
            print(f"[MATCHMAKING] =================================================================\n")
            return created
        
        print(f"[MATCHMAKING] ⏳ User waiting for more players...")
        print(f"[MATCHMAKING] =================================================================\n")
        return {"message": "Joined matchmaking queue"}
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[ERROR] Exception in join_matchmaking: {error_trace}")
        raise HTTPException(status_code=500, detail=f"Matchmaking error: {str(e)}")

def try_process_match(db: Session):
    """
    Check whole queue and create a room if we can satisfy REQUIRED composition.
    Returns created room info or None.
    """
    from sqlalchemy import func
    
    print(f"\n[MATCHMAKING] === try_process_match called ===")
    
    # read all queue entries
    queue_entries = get_all_queue(db)
    print(f"[MATCHMAKING] Total queue entries: {len(queue_entries) if queue_entries else 0}")
    
    if not queue_entries:
        print(f"[MATCHMAKING] Queue is empty, returning None")
        return None

    # group by role
    buckets: dict[str, list[int]] = {}
    for e in queue_entries:
        buckets.setdefault(e.role, []).append(e.user_id)

    print(f"[MATCHMAKING] Queue buckets: {buckets}")
    print(f"[MATCHMAKING] Required composition: {REQUIRED}")

    # quick check: do we have enough for every required role?
    roles_satisfied = True
    for needed_role, needed_count in REQUIRED.items():
        have = len(buckets.get(needed_role, []))
        print(f"[MATCHMAKING]   Role '{needed_role}': need {needed_count}, have {have}")
        if have < needed_count:
            print(f"[MATCHMAKING]   ❌ Not enough {needed_role}, cannot create room yet")
            roles_satisfied = False
            break
    
    if not roles_satisfied:
        print(f"[MATCHMAKING] Cannot satisfy requirements, returning None\n")
        return None

    print(f"[MATCHMAKING] ✅ All requirements satisfied, creating room...")
    
    # pick users for each role (randomly)
    selected_user_ids: list[int] = []
    for needed_role, needed_count in REQUIRED.items():
        candidates = buckets.get(needed_role, [])
        chosen = random.sample(candidates, needed_count)
        selected_user_ids.extend(chosen)
        print(f"[MATCHMAKING]   Selected {needed_role}: {chosen}")

    print(f"[MATCHMAKING] Final selected users: {selected_user_ids}")

    # create room (import Room model at runtime to avoid circular import)
    try:
        from app.db.database import SessionLocal  # not used, but ensure db utils available
        from app.rooms.model import Room
        from .models import RoomMember, RoomHistory
        from app.db.models import User
        
        print(f"[MATCHMAKING] Creating room with leader: {random.choice(selected_user_ids)}")
        
        # create Room record
        room = Room(leader_id=random.choice(selected_user_ids), current_count=len(selected_user_ids))
        db.add(room)
        db.commit()
        db.refresh(room)
        print(f"[MATCHMAKING] Room {room.id} created in database")
        
        # Get the User objects for the selected user IDs
        users = db.query(User).filter(User.id.in_(selected_user_ids)).all()
        
        # Add users to room members via room_users
        room.members.extend(users)
        print(f"[MATCHMAKING] Added users to room.members")
        
        # Also add to room_members table with role information AND room history
        from datetime import datetime
        for user_id in selected_user_ids:
            # Get the queue entry to get the role
            queue_entry = next((e for e in queue_entries if e.user_id == user_id), None)
            room_member = RoomMember(
                room_id=room.id,
                user_id=user_id,
                role=queue_entry.role if queue_entry else None,
                role_id=None  # Can be set later if needed
            )
            db.add(room_member)
            
            # Add room history entry
            room_history = RoomHistory(
                room_id=room.id,
                user_id=user_id,
                action="join",
                timestamp=datetime.now()
            )
            db.add(room_history)
        
        db.commit()
        print(f"[MATCHMAKING] Saved room members to database")
        
        # remove selected users from queue
        remove_many_from_queue(db, selected_user_ids)
        print(f"[MATCHMAKING] Removed users from queue")

        print(f"[MATCHMAKING] ✅ Room {room.id} created successfully!")
        print(f"[MATCHMAKING]   Leader: {room.leader_id}")
        print(f"[MATCHMAKING]   Members: {selected_user_ids}\n")

        return {
            "message": "Room created",
            "room_id": room.id,
            "leader_id": room.leader_id
        }
        
    except Exception as e:
        import traceback
        print(f"[ERROR] Error creating room: {traceback.format_exc()}")
        db.rollback()
        raise
