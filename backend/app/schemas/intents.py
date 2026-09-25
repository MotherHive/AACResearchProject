from pydantic import BaseModel


class IntentDefinitionRead(BaseModel):
    description: str
    specifics: dict[str, str]


class IntentsRead(BaseModel):
    intents: dict[str, IntentDefinitionRead]