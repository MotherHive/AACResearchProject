from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.database import Base, engine
from .db import models

from .routers import conversations, intents, routers

app = FastAPI(title="AAC API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    conversations.router,
    prefix="/api/v1",
)

app.include_router(
    intents.router,
    prefix="/api/v1",
)

app.include_router(
    responses.router, 
    prefix="/api/v1"
)