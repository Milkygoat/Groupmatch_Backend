"""
Migration script to add role and role_id columns to room_members table
"""
from sqlalchemy import text
from app.db.database import engine

def migrate():
    with engine.connect() as conn:
        try:
            # Check if columns already exist
            result = conn.execute(text("SHOW COLUMNS FROM room_members LIKE 'role'"))
            if result.fetchone():
                print("[MIGRATION] role column already exists")
            else:
                print("[MIGRATION] Adding role column...")
                conn.execute(text("ALTER TABLE room_members ADD COLUMN role VARCHAR(50) NULL"))
                print("[MIGRATION] ✅ role column added")
            
            result = conn.execute(text("SHOW COLUMNS FROM room_members LIKE 'role_id'"))
            if result.fetchone():
                print("[MIGRATION] role_id column already exists")
            else:
                print("[MIGRATION] Adding role_id column...")
                conn.execute(text("ALTER TABLE room_members ADD COLUMN role_id INT NULL"))
                print("[MIGRATION] ✅ role_id column added")
            
            conn.commit()
            print("[MIGRATION] ✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"[MIGRATION] ❌ Error: {str(e)}")
            conn.rollback()

if __name__ == "__main__":
    migrate()
