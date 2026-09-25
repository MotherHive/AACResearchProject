from fastapi import APIRouter

from ..schemas.intents import (
    IntentDefinitionRead,
    IntentsRead,
)
from ..domain.intents import INTENT_DEFINITIONS

router = APIRouter(
    prefix="/intents",
    tags=["intents"],
)


@router.get("", response_model=IntentsRead)
def get_intents():
    return IntentsRead(
        intents={
            name: IntentDefinitionRead(
                description=definition.description,
                specifics=definition.specifics,
            )
            for name, definition in INTENT_DEFINITIONS.items()
        }
    )