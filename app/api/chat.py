from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from app.core.therapist_agent import TherapistAgent
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str
    session_id: str | None = None

@router.post("/message")
async def send_message(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    agent = TherapistAgent(session_id=session_id, user_id=request.user_id)
    result = await agent.process_message(request.message)
    result["session_id"] = session_id
    return result

@router.websocket("/ws/{user_id}/{session_id}")
async def websocket_chat(websocket: WebSocket, user_id: str, session_id: str):
    await websocket.accept()
    agent = TherapistAgent(session_id=session_id, user_id=user_id)

    try:
        while True:
            data = await websocket.receive_json()
            user_message = data.get("message", "")

            from app.services.mood.mood_detector import mood_detector
            from app.core.coping_strategies import get_strategy, MUSIC_MOODS

            mood_analysis = mood_detector.analyze(user_message)
            await websocket.send_json({
                "type": "mood",
                "data": {
                    "mood": mood_analysis["primary_mood"],
                    "music": MUSIC_MOODS.get(mood_analysis["primary_mood"], MUSIC_MOODS["neutral"])
                }
            })

            async for chunk in agent.stream_response(user_message):
                await websocket.send_json({"type": "chunk", "data": chunk})

            strategy = get_strategy(mood_analysis["primary_mood"])
            await websocket.send_json({"type": "done", "data": {"coping_strategy": strategy}})

    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
