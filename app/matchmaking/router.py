from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from .service import join_matchmaking
from .schemas import JoinMatchmakingResponse
from app.db.models import Profile

from app.matchmaking.models import RoomMember, MatchmakingQueue

router = APIRouter(prefix="/matchmaking", tags=["Matchmaking"])

@router.post("/join", response_model=JoinMatchmakingResponse)
def join_queue(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        # ambil profile user
        print(f"[DEBUG] User {current_user.id} trying to join matchmaking")
        profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
        if not profile:
            print(f"[DEBUG] User {current_user.id} has no profile")
            raise HTTPException(status_code=400, detail="User belum membuat profile")

        print(f"[DEBUG] User {current_user.id} profile found, role: {profile.role}")
        result = join_matchmaking(
            db=db,
            user_id=current_user.id,
            role=profile.role
        )

        print(f"[DEBUG] Matchmaking result: {result}")
        
        # result bisa {"message": "..."} atau hasil create_room
        response = JoinMatchmakingResponse(
            message=result.get("message"),
            room_id=result.get("room_id"),
            leader_id=result.get("leader_id")
        )
        print(f"[DEBUG] Response created: {response}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"[ERROR] Matchmaking error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Matchmaking error: {str(e)}")

@router.get("/status")
def matchmaking_status(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # cek apakah user sudah punya room
    member = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id
    ).first()

    if member:
        return {
            "status": "matched",
            "room_id": member.room_id
        }

    # cek apakah user ada di queue
    in_queue = db.query(MatchmakingQueue).filter_by(
        user_id=current_user.id
    ).first()

    if in_queue:
        return {
            "status": "waiting"
        }

    return {
        "status": "idle"
    }


@router.delete("/queue/clear")
def clear_matchmaking_queue(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Remove current user from queue"""
    from .queue import remove_from_queue
    remove_from_queue(db, current_user.id)
    return {"message": "Removed from queue"}


@router.post("/leave")
def leave_matchmaking(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Leave matchmaking queue or room"""
    from .queue import remove_from_queue
    
    # Remove dari queue
    remove_from_queue(db, current_user.id)
    
    # Remove dari room juga (optional, untuk flexibility)
    member = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id
    ).first()
    
    if member:
        db.delete(member)
        db.commit()
        return {"message": "Left room"}
    
    return {"message": "Left queue"}
