from fastapi import APIRouter, UploadFile, File
from app.services.voice.whisper_service import whisper_service
from app.services.mood.mood_detector import mood_detector

router = APIRouter()

@router.post("/transcribe")
async def transcribe_voice(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    transcript = await whisper_service.transcribe(audio_bytes, audio.filename)
    mood = mood_detector.analyze(transcript["text"])

    return {
        "transcript": transcript["text"],
        "language": transcript.get("language"),
        "mood_detected": mood["primary_mood"],
        "sentiment_score": mood["sentiment_score"]
    }
