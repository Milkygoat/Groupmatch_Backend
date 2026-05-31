import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(".env.local")

from app.db.database import engine, Base

# Import all models to ensure they are registered with Base
import app.db.models
import app.rooms.model
import app.matchmaking.models

def reset():
    print("Mereset database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database berhasil direset (semua tabel kosong dan siap digunakan).")

if __name__ == "__main__":
    reset()
