from pydantic import BaseModel

class TopicGenerationRequest(BaseModel):
    clue: str

class TopicOptions(BaseModel):
    topics: list[str]