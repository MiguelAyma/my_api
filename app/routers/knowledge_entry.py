from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data._db_config import get_db
from app.schemas._error import ErrorType, raise_app_error
from app.schemas._knowledge_entry import KnowledgeEntryCreate, KnowledgeEntryImproved, KnowledgeEntryResponse, KnowledgeEntryUpdate
from app.service._knowledge_entry_crud import create_knowledge_entry_service, create_knowledge_entry_service2, update_knowledge_entry_service



router = APIRouter()

@router.post("/", response_model=KnowledgeEntryImproved, status_code=status.HTTP_201_CREATED)
def create_knowledge_entry_handler(data: KnowledgeEntryCreate, db: Session = Depends(get_db)):
    try:
        return create_knowledge_entry_service2(db, data)
    except Exception as ex:
        raise_app_error(
            error_code="CreateEntryFailed",
            message="An unexpected error occurred while creating the entry.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )


@router.put("/{entry_id}", response_model=KnowledgeEntryResponse)
def update_knowledge_entry_handler(entry_id: int, data: KnowledgeEntryUpdate, db: Session = Depends(get_db)):
    try:
        return update_knowledge_entry_service(db, entry_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
