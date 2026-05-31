"""
Test script to verify database schema
"""
from app.db.database import engine, Base
from app.matchmaking.models import RoomMember, MatchmakingQueue
from app.rooms.model import Room
from app.db.models import User, Profile

# Create all tables
print("[DB] Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("[DB] ✅ Tables created/verified")

# Check if room_members table has the columns
from sqlalchemy import inspect, text

inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"\n[DB] Available tables: {tables}")

if 'room_members' in tables:
    columns = [c['name'] for c in inspector.get_columns('room_members')]
    print(f"[DB] room_members columns: {columns}")
    
    if 'role' in columns and 'role_id' in columns:
        print("[DB] ✅ room_members has role and role_id columns")
    else:
        print("[DB] ⚠️ room_members missing role or role_id columns")
        print("[DB] Need to add columns manually or reset database")
