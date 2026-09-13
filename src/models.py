from dataclasses import dataclass, field


@dataclass
class ConversationTurn:
    speaker: str
    text: str

@dataclass 
class Intent:
    pass

@dataclass 
class ResponseContext:
    conversation: Conversation
    topics: list[str] | None = None
    intent: Intent | None = None


