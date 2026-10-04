from pydantic import BaseModel

class StreamingSessionResponse(BaseModel):
    token: str
    expires_in_seconds: int
    max_session_duration_seconds: int
