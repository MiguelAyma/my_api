
from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime

class ToneBase(BaseModel):
    name: str
    associated_emoji: str

class ToneCreate(ToneBase):
    pass

class ToneUpdate(BaseModel):
    name: Optional[str]
    associated_emoji: Optional[str]

class ToneResponse(ToneBase):
    tone_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
