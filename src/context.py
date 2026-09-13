from dataclasses import dataclass

@dataclass 
class ResponseContext:
    conversation: Conversation
    topics: list[str]
    intent: Intent | None


