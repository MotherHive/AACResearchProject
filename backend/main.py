from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db
from .models import Conversation
from .schemas import ConversationRead

app = FastAPI()
router = APIRouter(prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post(
    "/conversations",
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






app.include_router(router)