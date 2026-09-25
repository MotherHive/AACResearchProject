from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db.models import Conversation, Turn

from ..schemas.conversations import ConversationRead, TurnCreate, TurnRead

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


@router.post(
    "",
    response_model=ConversationRead,
    status_code=201,
)
def create_conversation(
    db: Session = Depends(get_db),
):
    conversation = Conversation()

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


@router.post(
    "/{conversation_id}/turns",
    response_model=TurnRead,
    status_code=201,
)
def create_turn(
    conversation_id: UUID,
    turn_data: TurnCreate,
    db: Session = Depends(get_db),
):
    conversation = db.get(Conversation, conversation_id)

    turn = Turn(
        speaker=turn_data.speaker,
        text=turn_data.text,
        sequence=len(conversation.turns) + 1,
    )

    conversation.turns.append(turn)

    db.commit()
    db.refresh(turn)

    return turn


   