from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict


class BusinessBase(BaseModel):
    business_name: str
    business_description: str

    whatsapp_url: Optional[str] = None
    instagram_url: Optional[str] = None
    facebook_url: Optional[str] = None
    tiktok_url: Optional[str] = None
    email: Optional[str] = None
    address:  Optional[str] = None
    address_url: Optional[str] = None

class BusinessResponse(BusinessBase):
    business_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DeleteBusinessResponse(BaseModel):
    message: str
    id: int

class BusinessNotFoundError(Exception):
    """
    Exception raised when a Business Business is not found in the database.
    """
    pass



    
    
    


