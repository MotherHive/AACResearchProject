from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import Conversation
from ..schemas.topics import TopicGenerationRequest, TopicOptions
from ..services.topic_generation.topic_generator import TopicGenerator
from ..services.topic_generation.inferred_topic_generator import InferredTopicGenerator

topic_generator = TopicGenerator()
inferred_topic_generator = InferredTopicGenerator()


router = APIRouter(
    prefix="/conversations",
    tags=["topics"],
)
@router.post(
    "/{conversation_id}/topics",
    response_model=TopicOptions,
)
def create_topic_options(
    conversation_id: UUID,
    request: TopicGenerationRequest,
    db: Session = Depends(get_db),
):
    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail=f"Conversation does not exist with id {conversation_id}",
        )

    existing = topic_generator.generate(
        turns=conversation.turns,
        clue=request.clue,
        excluded_topics=request.selected_topics,
    )

    inferred = inferred_topic_generator.generate(
        turns=conversation.turns,
        clue=request.clue,
        excluded_topics=request.selected_topics,
    )

    topics = existing[:3]
    return topics + [topic for topic in inferred if topic not in topics][:3]

    return TopicOptions(
        topics=topics,
    )
