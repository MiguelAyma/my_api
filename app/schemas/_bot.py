
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class BotBase(BaseModel):
    business_id: int
    name: str
    archetype_id: int
    formality_level: int
    proactivity_level: int
    response_length: int
    main_goal: str
    limiting_instructions: str
    version: str
    status: str
    tone_ids: List[int] = Field(..., description="List of Tone IDs to associate")

class BotCreate(BotBase):
    pass

class BotResponse(BaseModel):
    bot_id: int
    business_id: int
    name: str
    archetype_id: int
    formality_level: int
    proactivity_level: int
    response_length: int
    main_goal: str
    limiting_instructions: str
    version: str
    status: str
    created_at: datetime
    updated_at: datetime
    tone_ids: List[int]

    model_config = ConfigDict(from_attributes=True)


class BotUpdate(BaseModel):
    name: Optional[str]
    archetype_id: Optional[int]
    formality_level: Optional[int]
    proactivity_level: Optional[int]
    response_length: Optional[int]
    main_goal: Optional[str]
    limiting_instructions: Optional[str]
    version: Optional[str]
    status: Optional[str]
    tone_ids: Optional[List[int]]

    model_config = ConfigDict(from_attributes=True)
