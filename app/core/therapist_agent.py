from datetime import datetime
from typing import AsyncGenerator
from app.services.llm.groq_service import groq_service as ollama_service
from app.services.memory.langchain_memory import TherapistMemory
from app.services.memory.db_persistence import (
    ensure_user_exists, ensure_session_exists, save_message, update_session_mood
)
from app.services.mood.mood_detector import mood_detector
from app.core.prompt_templates import SYSTEM_PROMPT, CRISIS_RESPONSE
from app.core.coping_strategies import get_strategy, get_motivational_prompt, MUSIC_MOODS

class TherapistAgent:
    def __init__(self, session_id: str, user_id: str):
        self.memory = TherapistMemory(session_id, user_id)
        self.session_id = session_id
        self.user_id = user_id
        self.current_mood = "neutral"

    def _get_time_of_day(self) -> str:
        hour = datetime.now().hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 21: return "evening"
        else: return "night"

    def _build_system_prompt(self, mood: str, context: str) -> str:
        return SYSTEM_PROMPT.format(mood=mood, context=context, time_of_day=self._get_time_of_day())

    async def _ensure_db_records(self):
        await ensure_user_exists(self.user_id)
        await ensure_session_exists(self.session_id, self.user_id)

    async def process_message(self, user_message: str) -> dict:
        await self._ensure_db_records()

        mood_analysis = mood_detector.analyze(user_message)
        self.current_mood = mood_analysis["primary_mood"]

        if mood_analysis["is_crisis"]:
            self.memory.add_user_message(user_message)
            self.memory.add_ai_message(CRISIS_RESPONSE)
            await save_message(self.user_id, self.session_id, "user", user_message, "crisis", mood_analysis["sentiment_score"])
            await save_message(self.user_id, self.session_id, "assistant", CRISIS_RESPONSE, "crisis", None)
            return {
                "response": CRISIS_RESPONSE,
                "mood": "crisis",
                "is_crisis": True,
                "coping_strategy": None,
                "music": MUSIC_MOODS["sad"],
                "motivational_prompt": None
            }

        history = self.memory.get_history_as_list()
        context = self.memory.get_summary_context()
        system_prompt = self._build_system_prompt(self.current_mood, context)

        self.memory.add_user_message(user_message)
        history.append({"role": "user", "content": user_message})

        response = await ollama_service.chat(history, system_prompt)
        self.memory.add_ai_message(response)

        await save_message(self.user_id, self.session_id, "user", user_message, self.current_mood, mood_analysis["sentiment_score"])
        await save_message(self.user_id, self.session_id, "assistant", response, self.current_mood, None)
        await update_session_mood(self.session_id, self.current_mood, mood_analysis["sentiment_score"])

        strategy = get_strategy(self.current_mood)
        music = MUSIC_MOODS.get(self.current_mood, MUSIC_MOODS["neutral"])
        motivational = get_motivational_prompt() if mood_analysis["sentiment_score"] < -0.3 else None

        return {
            "response": response,
            "mood": self.current_mood,
            "sentiment_score": mood_analysis["sentiment_score"],
            "is_crisis": False,
            "coping_strategy": strategy,
            "music": music,
            "motivational_prompt": motivational
        }

    async def stream_response(self, user_message: str) -> AsyncGenerator:
        await self._ensure_db_records()

        mood_analysis = mood_detector.analyze(user_message)
        self.current_mood = mood_analysis["primary_mood"]

        if mood_analysis["is_crisis"]:
            await save_message(self.user_id, self.session_id, "user", user_message, "crisis", mood_analysis["sentiment_score"])
            await save_message(self.user_id, self.session_id, "assistant", CRISIS_RESPONSE, "crisis", None)
            yield CRISIS_RESPONSE
            return

        history = self.memory.get_history_as_list()
        context = self.memory.get_summary_context()
        system_prompt = self._build_system_prompt(self.current_mood, context)

        self.memory.add_user_message(user_message)
        history.append({"role": "user", "content": user_message})

        full_response = ""
        async for chunk in ollama_service.chat_stream(history, system_prompt):
            full_response += chunk
            yield chunk

        self.memory.add_ai_message(full_response)

        await save_message(self.user_id, self.session_id, "user", user_message, self.current_mood, mood_analysis["sentiment_score"])
        await save_message(self.user_id, self.session_id, "assistant", full_response, self.current_mood, None)
        await update_session_mood(self.session_id, self.current_mood, mood_analysis["sentiment_score"])
