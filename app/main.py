from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import (
    category,
    item,
    user,
    business,
    bot,
    archetype,
    tone,
    knowledge_entry,
)

app = FastAPI(
    title="My API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz
@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(business.router, prefix="/api/v1/business", tags=["Business"])
app.include_router(category.router, prefix="/api/v1/category", tags=["Category"])
app.include_router(item.router, prefix="/api/v1/item", tags=["Item"])
app.include_router(bot.router, prefix="/api/v1/bot", tags=["Bot"])
app.include_router(archetype.router, prefix="/api/v1/archetype", tags=["Archetype"])
app.include_router(tone.router, prefix="/api/v1/tone", tags=["Tone"])
app.include_router(knowledge_entry.router, prefix="/api/v1/knowledge-entry", tags=["Knowledge Entry"]) 