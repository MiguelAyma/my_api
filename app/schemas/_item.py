from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class ItemBase(BaseModel):

    business_id: int
    item_name: str
    item_description: str
    price: float
    price_discount: float
    is_visible: bool
    categories: List[int]  
    
    
class ItemResponse(ItemBase):
    item_id: int
    item_slug: str
    created_at: datetime
    updated_at: datetime
    
class DeleteItemResponse(BaseModel):
    message: str
    id: int

class ItemNotFoundError(Exception):
    """
    Exception raised when a Item item is not found in the database.
    """
    pass