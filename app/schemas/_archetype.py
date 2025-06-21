from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ArchetypeBase(BaseModel):
    name: str
    description: Optional[str]
    icon: Optional[str]

class ArchetypeCreate(ArchetypeBase):
    pass

class ArchetypeUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    icon: Optional[str]

class ArchetypeResponse(ArchetypeBase):
    archetype_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
