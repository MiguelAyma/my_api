from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

#from app.data._sqlalchemy_models import business
from app.models.sql_alchemy_models import Business 
from app.data._business_crud import create_business_data,update_business_data,get_business_data
from app.schemas._business import BusinessBase, BusinessResponse
from app.schemas._error import ErrorType, raise_app_error

def create_business_service(
        business_create: BusinessBase,
        user_id: str,
        db:Session
    ) -> BusinessResponse:

    try:
        db_business = Business(
            user_id = user_id,
            business_name = business_create.business_name,
            business_description = business_create.business_description,
            facebook_url = business_create.facebook_url,
            instagram_url = business_create.instagram_url,
            tiktok_url=business_create.tiktok_url,
            email=business_create.email,
            whatsapp_url=business_create.whatsapp_url,
            address=business_create.address,
            address_url=business_create.address_url
        )

        record: Business = create_business_data(db_business, db)

        return BusinessResponse(
            business_id=record.business_id,
            business_name = record.business_name,
            business_description = record.business_description,
            facebook_url = record.facebook_url,
            instagram_url = record.instagram_url,
            tiktok_url=record.tiktok_url,
            email=record.email,
            whatsapp_url=record.whatsapp_url,
            address=record.address,
            address_url=record.address_url,
            created_at = record.created_at,
            updated_at = record.updated_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="BusinessServiceError",
            message="Failed to create business in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )

def update_business_service(
    business_update: BusinessBase,
    business_id: int,
    user_id: str,
    db: Session
) -> BusinessResponse:
    """
    Update an existing Business and invalidate related cache if necessary.

    Args:
        Business_update (BusinessBase): Updated data for the Business.
        Business_id (int): ID of the Business to update.
        user_id (str): ID of the user who owns the Business.
        db (Session): SQLAlchemy database session.

    Returns:
        BusinessResponse: Data of the updated Business.

    Raises:
        HTTPException: If the Business does not exist or update fails.
    """
    try:
        db_business = BusinessBase(
            user_id=user_id,
            business_name = business_update.business_name,
            business_description = business_update.business_description,
            facebook_url = business_update.facebook_url,
            instagram_url = business_update.instagram_url,
            tiktok_url=business_update.tiktok_url,
            email=business_update.email,
            whatsapp_url=business_update.whatsapp_url,
            address=business_update.address,
            address_url=business_update.address_url
        )
        record: Business = update_business_data(
            db=db,
            business_data=db_business,
            user_id=user_id,
            business_id=business_id
        )

        return BusinessResponse(
            business_id=record.business_id,
            business_name = record.business_name,
            business_description = record.business_description,
            facebook_url = record.facebook_url,
            instagram_url = record.instagram_url,
            tiktok_url=record.tiktok_url,
            email=record.email,
            whatsapp_url=record.whatsapp_url,
            address=record.address,
            address_url=record.address_url,
            created_at = record.created_at,
            updated_at = record.updated_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="BusinessServiceError",
            message="Failed to update Business in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )
def get_business_service(db: Session, user_id:str ,business_id: int) -> BusinessResponse:
    """
    Obtiene un registro de Business por su ID.
    
    Args:
        db (Session): Sesión de la base de datos.
        Business_id (int): ID del negocio.
    
    Returns:
        BusinessResponse: El registro de Business en formato Pydantic.
    """
    try:
        record:Business = get_business_data( user_id,business_id, db)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Business not found"
            )
        
        # Convertir el modelo SQLAlchemy a Pydantic
        return BusinessResponse(
            business_id=record.business_id,
            business_name = record.business_name,
            business_description = record.business_description,

            facebook_url = record.facebook_url,
            instagram_url = record.instagram_url,
            tiktok_url=record.tiktok_url,
            email=record.email,
            whatsapp_url=record.whatsapp_url,
            address=record.address,
            address_url=record.address_url,
            created_at = record.created_at,
            updated_at = record.updated_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="BusinessServiceError",
            message="Failed to get Business in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )