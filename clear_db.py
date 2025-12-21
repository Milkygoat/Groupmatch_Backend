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
    conn.commit()

db.query(Room).delete()
db.commit()
print('✅ Database cleared for fresh test')
db.close()
