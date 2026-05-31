import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(".env.local")

from app.db.database import SessionLocal
from app.matchmaking.models import MatchmakingQueue
from app.db.models import Profile
from app.rooms.model import Room

def check():
    db = SessionLocal()
    print("--- QUEUE ---")
    for q in db.query(MatchmakingQueue).all():
        print(f"User: {q.user_id}, Role: '{q.role}'")
        
    print("--- PROFILES ---")
    for p in db.query(Profile).all():
        print(f"User: {p.user_id}, Role: '{p.role}'")

if __name__ == "__main__":
    check()
