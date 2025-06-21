from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data._db_config import get_db
from app.schemas._tone import ToneCreate, ToneResponse, ToneUpdate
from app.service._tone_crud import create_tone_service, get_all_tones_service, update_tone_service



router = APIRouter()

@router.get("/", response_model=list[ToneResponse])
def get_all_tones_handler(db: Session = Depends(get_db)):
    return get_all_tones_service(db)

@router.post("/", response_model=ToneResponse, status_code=status.HTTP_201_CREATED)
def create_tone_handler(data: ToneCreate, db: Session = Depends(get_db)):
    return create_tone_service(db, data)

@router.put("/{tone_id}", response_model=ToneResponse)
def update_tone_handler(tone_id: int, data: ToneUpdate, db: Session = Depends(get_db)):
    try:
        return update_tone_service(db, tone_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
