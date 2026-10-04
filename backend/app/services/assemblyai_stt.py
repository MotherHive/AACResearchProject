import os
from dotenv import load_dotenv
import httpx

from ..schemas.stt import StreamingSessionResponse

load_dotenv()

ASSEMBLY_TOKEN_ENDPOINT = "https://streaming.assemblyai.com/v3/token"
REDEMPTION_LIFETIME = 30 # seconds
MAX_SESSION_DURATION = 900 # seconds

async def get_streaming_token():
    api_key = os.getenv("ASSEMBLYAI_API_KEY")

    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(
            ASSEMBLY_TOKEN_ENDPOINT,
            params={
                "expires_in_seconds": REDEMPTION_LIFETIME,
                "max_session_duration_seconds": MAX_SESSION_DURATION,
            },
            headers={
                "Authorization": api_key,
            },
        )
        
    payload = response.json()

    token = payload.get("token")
    expires_in_seconds = payload.get("expires_in_seconds")

    return StreamingSessionResponse(
        token=token,
        expires_in_seconds=expires_in_seconds,
        max_session_duration_seconds=MAX_SESSION_DURATION
    )