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

    "feedback": IntentDefinition(
        description="Provide agreement/disagreement.",
        specifics={
            "agree": "State agreement",
            "disagree": "State disagreement",
            "unsure": "State unsurity",
        },
    ),

    "fix": IntentDefinition(
        description="Repair or clarify a conversational element.",
        specifics={
            "clarify": "Ensure understanding",
            "fix": "Fix a misunderstanding",
            "repeat": "Ask to say again",
        },
    ),

    "inform": IntentDefinition(
        description="Tell the partner about something or introduce a topic.",
        specifics={
            "agree": "State agreement",
            "disagree": "State disagreement",
            "unsure": "State unsurity",
        },
    ),

    "emotion": IntentDefinition(
        description="Express a feeling about something.",
        specifics={
            "agree": "State agreement",
            "disagree": "State disagreement",
            "unsure": "State unsurity",
        },
    )
    # 
    #
}



@dataclass(frozen=True, slots=True)
class Intent:
    primary: str
    specific: str | None = None

    def __post_init__(self) -> None:
        if self.primary is not None and self.primary not in INTENT_DEFINITIONS:
            raise ValueError(
                f"Unknown primary intent: {self.primary}"
            )

        if self.specific is not None and self.primary is not None:
            if self.specific not in INTENT_DEFINITIONS[self.primary].specifics:
                raise ValueError(
                    f"Specific intent '{self.specific}' not in '{self.primary}'"
                )

    @property
    def primary_description(self) -> str:
        if self.primary is None:
            return None
            
        return INTENT_DEFINITIONS[self.primary].description

    @property
    def specific_description(self) -> str | None:
        if self.specific is None:
            return None

        return INTENT_DEFINITIONS[self.primary].specifics[self.specific]

    @staticmethod
    def available_primaries() -> dict[str, str]:
        primaries = {}

        for primary in INTENT_DEFINITIONS.keys():
            primaries[primary] = INTENT_DEFINITIONS[primary].description
        
        return primaries

    @staticmethod
    def available_specifics(primary) -> dict[str, str]:
        return INTENT_DEFINITIONS[primary].specifics
