from app.db.database import SessionLocal, engine
from app.matchmaking.models import MatchmakingQueue
from app.rooms.model import Room
from app.matchmaking.models import RoomMember
from sqlalchemy import text

db = SessionLocal()

# Delete in correct order due to foreign keys
db.query(MatchmakingQueue).delete()
db.query(RoomMember).delete()

# Delete room_users entries
with engine.connect() as conn:
    conn.execute(text("DELETE FROM room_users"))
    conn.execute(text("DELETE FROM room_history"))
    conn.execute(text("DELETE FROM rooms"))
    conn.execute(text("DELETE FROM profile"))
    conn.execute(text("DELETE FROM auth"))
    conn.commit()

db.commit()
print('✅ Database fully cleared (auth, profile, rooms, queue, members, history)')
db.close()
