from dataclasses import dataclass

@dataclass 
class ResponseContext:
    conversation: Conversation
    topics: list[str] | None = None
    intent: Intent | None = None


