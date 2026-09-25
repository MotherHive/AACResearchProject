from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..schemas.speech import SpeechRequest
from ..services.tts_stream import stream_speech


router = APIRouter(prefix="/speech", tags=["speech"])

@router.post("")
def create_speech(request: SpeechRequest):
    return StreamingResponse(
        stream_speech(request.text),
        media_type="application/octet-stream",
        headers={
            "X-Audio-Format": "pcm_s16le",
            "X-Sample-Rate": "24000",
            "X-Audio-Channels": "1",
        },
    )