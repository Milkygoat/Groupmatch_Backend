from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    profile = relationship("Profile", back_populates="user", uselist=False)
    rooms_led = relationship("Room", back_populates="leader")


    room_members = relationship(
        "RoomMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth.id"), unique=True)

    name = Column(String(100))
    birthdate = Column(Date)
    role = Column(String(50))
    pict = Column(String(255))
    skill = Column(String(255))

    user = relationship("User", back_populates="profile")