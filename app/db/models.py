from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base

class User(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
