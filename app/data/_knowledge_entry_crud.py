from sqlalchemy.orm import Session
from app.models.sql_alchemy_models import KnowledgeEntries
from app.schemas._error import ErrorType, raise_app_error
from app.schemas._knowledge_entry import KnowledgeEntryCreate, KnowledgeEntryDBModel, KnowledgeEntryUpdate
import datetime
from sqlalchemy.exc import SQLAlchemyError
def create_knowledge_entry(db: Session, data: KnowledgeEntryDBModel) -> KnowledgeEntries:
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        entry = KnowledgeEntries(
            business_id=data.business_id,
            title=data.title,
            content=data.content,
            content_type=data.content_type,
            icon=data.icon,
            improved_title=data.improved_title,
            improved_content=data.improved_content, 
            categories=data.categories,
            created_at=now,
            updated_at=now
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    except SQLAlchemyError as e:
        db.rollback()
        raise_app_error(
            error_code="DatabaseEntryError",
            message="Failed to insert the new Entry into the database.",
            error_type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "insert",
                "model": "Entry"
            }
        )
def update_knowledge_entry(db: Session, entry_id: int, data: KnowledgeEntryUpdate) -> KnowledgeEntries:
    entry = db.query(KnowledgeEntries).filter(KnowledgeEntries.entry_id == entry_id).first()
    if not entry:
        raise ValueError(f"Knowledge entry with ID {entry_id} not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)

    entry.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(entry)
    return entry
