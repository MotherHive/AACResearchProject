from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    SmallInteger,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    turns: Mapped[list["Turn"]] = relationship(
        back_populates="conversation",
        order_by="Turn.sequence",
    )


class Turn(Base):
    __tablename__ = "turns"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )

    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id"),
    )

    speaker: Mapped[str] = mapped_column(
        String(20)
    )

    sequence: Mapped[int] = mapped_column(
        SmallInteger
    )

    text: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="turns"
    )

