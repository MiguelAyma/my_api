from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data._db_config import get_db
from app.schemas._archetype import ArchetypeCreate, ArchetypeUpdate, ArchetypeResponse
from app.service._archetype_crud import create_archetype_service, get_all_archetypes_service, update_archetype_service

router = APIRouter()

@router.post("/", response_model=ArchetypeResponse, status_code=status.HTTP_201_CREATED)
def create_archetype_handler(data: ArchetypeCreate, db: Session = Depends(get_db)):
    return create_archetype_service(db, data)

@router.put("/{archetype_id}", response_model=ArchetypeResponse)
def update_archetype_handler(archetype_id: int, data: ArchetypeUpdate, db: Session = Depends(get_db)):
    try:
        return update_archetype_service(db, archetype_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/", response_model=List[ArchetypeResponse])
def get_all_archetypes_handler(db: Session = Depends(get_db)):
    return get_all_archetypes_service(db)