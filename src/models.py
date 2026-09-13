from dataclasses import dataclass, field


@dataclass
class ConversationTurn:
    speaker: str
    text: str

@dataclass 
class Intent:
    primary: str
    specific: str | None = None

@dataclass 
class ResponseContext:
    conversation: Conversation
    topics: list[str] | None = None
    intent: Intent | None = None


