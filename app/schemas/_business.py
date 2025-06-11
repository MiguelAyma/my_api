from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas._error import ErrorType, raise_app_error


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
    
    @field_validator('business_name')
    def validate_business_name_length(cls, v):
        """Valida que el nombre del negocio no exceda los 200 caracteres."""
        max_len = 100
        if len(v) > max_len:
            raise_app_error(
                error_code="BusinessNameTooLong",
                message=f"El nombre del negocio no puede exceder los {max_len} caracteres.",
                error_type=ErrorType.VALIDATION,
                status_code=422
            )
        return v

    @field_validator('business_description')
    def validate_business_description_length(cls, v):
        """Valida que la descripción del negocio no exceda los 900 caracteres."""
        max_len = 800
        if len(v) > max_len:
            raise_app_error(
                error_code="BusinessDescriptionTooLong",
                message=f"La descripción del negocio no puede exceder los {max_len} caracteres.",
                error_type=ErrorType.VALIDATION,
                status_code=422
            )
        return v

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



    
    
    


