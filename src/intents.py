from dataclasses import dataclass

@dataclass
class IntentDefinition:
    description: str
    specifics: dict[str, str]


INTENT_DEFINITIONS = {
    "question": IntentDefinition(
        description="Ask a question to learn information. Not rhetorical or a command.",
        specifics={
            "ask_detail": "Ask for a specific detail.",
            "ask_reason": "Ask why something happened.",
            "ask_confirmation": "Ask whether something is correct.",
        },
    ),
    "action": IntentDefinition(
        description="Communicate about an action someone may take.",
        specifics={
            "request": "Ask the partner to provide, allow, or do something.",
            "suggest": "Propose an action someone other than the user should do.",
            "offer": "Offer to provide or do something.",
        },
    ),
}



@dataclass(frozen=True, slots=True)
class Intent:
    primary: str
    specific: str | None = None

    def __post_init__(self) -> None:
        if self.primary not in INTENT_DEFINITIONS:
            raise ValueError(
                f"Unknown primary intent: {self.primary}"
            )

        if self.specific is not None and self.specific not in definition.moves:
            raise ValueError(
                f"Specific intent '{self.specific}' not in '{self.primary}'"
            )

    @property
    def primary_description(self) -> str:
        return INTENT_DEFINITIONS[self.primary].description

    @property
    def specific_description(self) -> str | None:
        if self.specific is None:
            return None

        return INTENT_DEFINITIONS[self.primary].specifics[self.specific]


    @property
    def available_primaries(self) -> dict[str, str]:
        primaries = {}

        for primary in INTENT_DEFINITIONS.keys:
            primaries[primary] = INTENT_DEFINITIONS[primary].description
        
        return primaries


    @property
    def available_specifics(self) -> dict[str, str]:
        return INTENT_DEFINITIONS[self.primary].specifics
