from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.data._db_config import get_db
from app.schemas._bot import BotCreate, BotResponse, BotUpdate
from app.service._bot_crud import create_bot_service, update_bot_service

router = APIRouter()
@router.post("/", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
def create_bot_handler(bot_data: BotCreate, db: Session = Depends(get_db)):
    return create_bot_service(db, bot_data)


@router.put("/{bot_id}", response_model=BotResponse)
def update_bot_handler(bot_id: int, update_data: BotUpdate, db: Session = Depends(get_db)):
    try:
        return update_bot_service(db, bot_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))