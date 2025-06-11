from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import (
    category,
    user,
    business
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












