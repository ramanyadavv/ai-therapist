from fastapi import APIRouter
import uuid

router = APIRouter()

@router.post("/create")
async def create_user():
    return {"user_id": str(uuid.uuid4())}
