from fastapi import APIRouter
from pydantic import BaseModel
from app.services.mood.mood_detector import mood_detector

router = APIRouter()

class MoodRequest(BaseModel):
    text: str

@router.post("/analyze")
async def analyze_mood(request: MoodRequest):
    return mood_detector.analyze(request.text)
