from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class TurnCreate(BaseModel):
    speaker: Literal["user", "partner"]
    text: str


class TurnRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    speaker: str
    sequence: int
    text: str
    created_at: datetime


