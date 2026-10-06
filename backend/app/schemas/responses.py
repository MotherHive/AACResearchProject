from pydantic import BaseModel, ConfigDict, Field


class IntentSelection(BaseModel):
    primary: str
    specific: str | None = None


class ResponseGenerationRequest(BaseModel):
    topics: list[str] = Field(default_factory=list)
    intent: IntentSelection | None = None


class ResponseOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    responses: list[str] = Field(min_length=1, max_length=4)


class ResponseDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    established_facts: list[str]
    active_subject: str
    current_exchange: str
    responses: list[str] = Field(min_length=1, max_length=4)
