from sqlalchemy.orm import Session
from app.schemas._archetype import ArchetypeCreate, ArchetypeUpdate, ArchetypeResponse
from app.data._archetype_crud import create_archetype, get_all_archetypes, update_archetype

def create_archetype_service(db: Session, data: ArchetypeCreate) -> ArchetypeResponse:
    archetype = create_archetype(db, data)
    return ArchetypeResponse.model_validate(archetype)

def update_archetype_service(db: Session, archetype_id: int, data: ArchetypeUpdate) -> ArchetypeResponse:
    archetype = update_archetype(db, archetype_id, data)
    return ArchetypeResponse.model_validate(archetype)

def get_all_archetypes_service(db: Session) -> list[ArchetypeResponse]:
    archetypes = get_all_archetypes(db)
    return [ArchetypeResponse.model_validate(a) for a in archetypes]
