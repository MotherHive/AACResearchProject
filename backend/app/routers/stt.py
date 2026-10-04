from fastapi import APIRouter, Response

from ..schemas.stt import StreamingSessionResponse
from ..services.assemblyai_stt import get_streaming_token


router = APIRouter(prefix="/stt", tags=["stt"])

@router.post("/sessions", response_model=StreamingSessionResponse)
async def create_stt_session(response: Response):
    session = await get_streaming_token()

    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"

    return session