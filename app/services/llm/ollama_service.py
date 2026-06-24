import httpx
import json
from typing import AsyncGenerator
from app.config import settings

class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    async def chat_stream(self, messages: list, system_prompt: str) -> AsyncGenerator[str, None]:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "stream": True,
            "options": {"temperature": 0.7, "top_p": 0.9, "repeat_penalty": 1.1}
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if not data.get("done"):
                                yield data["message"]["content"]
                        except json.JSONDecodeError:
                            continue

    async def chat(self, messages: list, system_prompt: str) -> str:
        full_response = ""
        async for chunk in self.chat_stream(messages, system_prompt):
            full_response += chunk
        return full_response

ollama_service = OllamaService()
