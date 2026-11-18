from pydantic import BaseModel, Field

class TopicGenerationRequest(BaseModel):
    clue: str
    selected_topics: list[str] = Field(default_factory=list)

class TopicOptions(BaseModel):
    topics: list[str]
