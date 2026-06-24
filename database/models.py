from sqlalchemy import Column, String, Text, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    preferences = Column(JSON, default={})

    sessions = relationship("TherapySession", back_populates="user")
    messages = relationship("Message", back_populates="user")

class TherapySession(Base):
    __tablename__ = "therapy_sessions"

    id = Column(String(100), primary_key=True)
    user_id = Column(String(100), ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    dominant_mood = Column(String(50))
    mood_score = Column(Float)
    session_summary = Column(Text)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(100), primary_key=True)
    user_id = Column(String(100), ForeignKey("users.id"))
    session_id = Column(String(100), ForeignKey("therapy_sessions.id"))
    role = Column(String(20))
    content = Column(Text, nullable=False)
    mood_detected = Column(String(50))
    sentiment_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
    session = relationship("TherapySession", back_populates="messages")
