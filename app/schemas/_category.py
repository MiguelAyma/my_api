
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class CategoryBase(BaseModel):
    business_id: int
    category_name: str
    icon: int
    
class CategoryResponse(CategoryBase):
    category_id: int
    created_at: datetime
    updated_at: datetime
    
class DeleteCategoryResponse(BaseModel):
    message: str
    id: int

class CategoryNotFoundError(Exception):
    """
    Exception raised when a Category item is not found in the database.
    """
    pass