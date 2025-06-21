from sqlalchemy.orm import Session
from app.models.sql_alchemy_models import Archetype
from app.schemas._archetype import ArchetypeCreate, ArchetypeUpdate
import datetime

def create_archetype(db: Session, data: ArchetypeCreate) -> Archetype:
    now = datetime.datetime.now(datetime.timezone.utc)
    archetype = Archetype(
        name=data.name,
        description=data.description,
        icon=data.icon,
        created_at=now,
        updated_at=now
    )
    db.add(archetype)
    db.commit()
    db.refresh(archetype)
    return archetype

def update_archetype(db: Session, archetype_id: int, data: ArchetypeUpdate) -> Archetype:
    archetype = db.query(Archetype).filter(Archetype.archetype_id == archetype_id).first()
    if not archetype:
        raise ValueError(f"Archetype with ID {archetype_id} not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(archetype, field, value)
    
    archetype.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(archetype)
    return archetype

def get_all_archetypes(db: Session) -> list[Archetype]:
    return db.query(Archetype).order_by(Archetype.name).all()
