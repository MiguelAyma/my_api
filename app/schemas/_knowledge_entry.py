from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class KnowledgeEntryBase(BaseModel):
    business_id: int
    title: str
    content: str
    content_type: str

class KnowledgeEntryCreate(KnowledgeEntryBase):
    pass

class KnowledgeEntryUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    content_type: Optional[str]
    
class KnowledgeEntryImproved(KnowledgeEntryBase):
    entry_id: int
    improved_title: str
    improved_content: str
    categories: list[str]
    created_at: datetime
    updated_at: datetime
    icon: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
    
class KnowledgeEntryResponse(KnowledgeEntryBase):
    entry_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
    
class ImprovedEntryData(BaseModel):
    """
    Modelo que define la estructura de datos mejorada por el agente de IA.
    """
    improved_title: str = Field(description="Un título mejorado, conciso y atractivo para la entrada.")
    improved_content: str = Field(description="El contenido original, pero mejorado en claridad, formato y redacción.")
    icon: str = Field(description="El nombre de un ícono seleccionado de la lista proporcionada.")
    categories: List[str] = Field(
        description="Una lista de 2 a 5 categorías relevantes. Cada categoría debe tener el formato 'emoji nombre_categoria'."
    )

# Un modelo intermedio para pasar los datos combinados a la función de creación en BD
class KnowledgeEntryDBModel(KnowledgeEntryCreate):
    improved_title: str
    improved_content: str
    icon: str
    categories: list[str]