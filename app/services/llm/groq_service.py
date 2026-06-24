from groq import AsyncGroq
from app.config import settings

class GroqService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = "openai/gpt-oss-20b"

    async def chat_stream(self, messages: list, system_prompt: str):
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=0.7,
            stream=True
        )
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    async def chat(self, messages: list, system_prompt: str) -> str:
        full_response = ""
        async for chunk in self.chat_stream(messages, system_prompt):
            full_response += chunk
        return full_response

groq_service = GroqService()
