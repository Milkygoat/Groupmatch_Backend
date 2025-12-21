from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime, Table, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


room_users = Table(
    "room_users",
    Base.metadata,
    Column("room_id", ForeignKey("rooms.id"), primary_key=True),
    Column("user_id", ForeignKey("auth.id"), primary_key=True),
)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum("active", "closed", name="room_status"), default="active")

    capacity = Column(Integer, default=6)
    current_count = Column(Integer, default=0)

    leader_id = Column(Integer, ForeignKey("auth.id"), nullable=True)
    leader = relationship("User", back_populates="rooms_led")
    
    # Relationship to users melalui room_users table
    members = relationship(
        "User",
        secondary="room_users",
        back_populates="rooms"
    )
    
    # Relationship to room members dengan role info
    room_members = relationship("RoomMember", back_populates="room")