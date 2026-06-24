import openai
import tempfile
import os
from app.config import settings

class WhisperService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.webm") -> dict:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            with open(tmp_path, "rb") as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
            return {"text": transcript.text, "language": transcript.language, "duration": transcript.duration}
        finally:
            os.unlink(tmp_path)

whisper_service = WhisperService()
