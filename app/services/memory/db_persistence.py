from datetime import datetime
from sqlalchemy import select
from database.db import AsyncSessionLocal
from database.models import User, TherapySession, Message
import uuid

async def ensure_user_exists(user_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(id=user_id)
            session.add(user)
            await session.commit()

async def ensure_session_exists(session_id: str, user_id: str):
    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(select(TherapySession).where(TherapySession.id == session_id))
        therapy_session = result.scalar_one_or_none()
        if not therapy_session:
            therapy_session = TherapySession(id=session_id, user_id=user_id)
            db_session.add(therapy_session)
            await db_session.commit()

async def save_message(user_id: str, session_id: str, role: str, content: str, mood: str = None, sentiment_score: float = None):
    async with AsyncSessionLocal() as db_session:
        message = Message(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            role=role,
            content=content,
            mood_detected=mood,
            sentiment_score=sentiment_score
        )
        db_session.add(message)
        await db_session.commit()

async def update_session_mood(session_id: str, mood: str, mood_score: float):
    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(select(TherapySession).where(TherapySession.id == session_id))
        therapy_session = result.scalar_one_or_none()
        if therapy_session:
            therapy_session.dominant_mood = mood
            therapy_session.mood_score = mood_score
            await db_session.commit()

async def get_message_history(user_id: str, session_id: str, limit: int = 20):
    async with AsyncSessionLocal() as db_session:
        result = await db_session.execute(
            select(Message)
            .where(Message.user_id == user_id, Message.session_id == session_id)
            .order_by(Message.created_at)
            .limit(limit)
        )
        messages = result.scalars().all()
        return [{"role": m.role, "content": m.content} for m in messages]
