from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.database import Base

class MatchmakingQueue(Base):
    __tablename__ = "matchmaking_queue"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth.id", ondelete="CASCADE"))
    role = Column(String(50))
    joined_at = Column(TIMESTAMP)


class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("auth.id", ondelete="CASCADE"))
    role = Column(String(50))

    room = relationship("Room", back_populates="members")
    user = relationship("User", back_populates="room_members")


class RoomHistory(Base):
    __tablename__ = "room_history"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("auth.id", ondelete="CASCADE"))
    action = Column(Enum("join", "leave", "closed", name="history_action"))
    timestamp = Column(TIMESTAMP)