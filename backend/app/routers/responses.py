from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db.models import Conversation
from ..schemas.responses import (
    ResponseGenerationRequest,
    ResponseOptions,
)
from ..services.response_generator import generate_responses

router = APIRouter(
    prefix="/conversations",
    tags=["responses"],
)

@router.post(
    "/{conversation_id}/responses",
    response_model=ResponseOptions,
)
def create_response_options(
    conversation_id: UUID,
    request: ResponseGenerationRequest,
    db: Session = Depends(get_db),
):
    conversation = db.get(Conversation, conversation_id)

    return generate_responses(
        turns=conversation.turns,
        request=request,
    )