from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, Header, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.schemas._error import ErrorType, raise_app_error
from app.data._db_config import get_db
from utils._user_validation import get_current_user
from app.schemas._business import BusinessBase, BusinessResponse, DeleteBusinessResponse
from app.service._business_crud import create_business_service, delete_business_service, get_all_businesses_by_user_service,update_business_service, get_business_service



api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
router = APIRouter()

@router.post("/", response_model=BusinessResponse)
async def insert_business(
    business: BusinessBase,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user), 
) -> BusinessResponse:

    try :
        return create_business_service(
            business_create = business,
            user_id = user_id,
            db = db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="CreateBusinessFailed",
            message="An unexpected error occurred while creating the Business.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
@router.put(
    "/{business_id}",
    response_model=BusinessResponse,
    summary="Update an existing Business",
    response_description="The updated Business",
    status_code=status.HTTP_200_OK
)
async def update_business(
    business_id: int,
    business_update: BusinessBase,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) -> BusinessResponse:
    """
    Endpoint to update an existing Business by its ID.

    Args:
        Business_id (int): ID of the Business to update.
        Business_update (BusinessBase): New data to update the Business.
        db (Session): SQLAlchemy database session dependency.
        user_id (str): ID of the authenticated user (extracted from the token).

    Returns:
        BusinessResponse: The updated Business data.

    Raises:
        HTTPException:
            - 404: If the Business is not found or doesn't belong to the user.
            - 500: If an unexpected error occurs.
    """
    try:
        return update_business_service(
            business_update=business_update,
            business_id=business_id,
            user_id=user_id,
            db=db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="UpdateBusinessFailed",
            message="An unexpected error occurred while updating the Business.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
        
@router.get(
    "/{business_id}",
    response_model=BusinessResponse,
    summary="get an existing Business",
    response_description="Get Business",
    status_code=status.HTTP_200_OK
)
async def get_business(
    business_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) -> BusinessResponse:
    """
    Endpoint to update an existing Business by its ID.

    Args:
        Business_id (int): ID of the Business to update.
        Business_update (BusinessBase): New data to update the Business.
        db (Session): SQLAlchemy database session dependency.
        user_id (str): ID of the authenticated user (extracted from the token).

    Returns:
        BusinessResponse: The updated Business data.

    Raises:
        HTTPException:
            - 404: If the Business is not found or doesn't belong to the user.
            - 500: If an unexpected error occurs.
    """
    try:
        return get_business_service(
            business_id=business_id,
            user_id=user_id,
            db=db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="getBusinessFailed",
            message="An unexpected error occurred while get the Business.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
        
@router.delete(
    "/{business_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Business",
    response_model=DeleteBusinessResponse
)
def delete_business(
        business_id: int,
        db: Session = Depends(get_db),
        user_id: str = Depends(get_current_user)
    )->DeleteBusinessResponse:
    """
    Delete a Single Business item

    Args:
        todo_id (UUID): TODO ID
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        null
    """
    try:

        return delete_business_service(
            business_id, 
            db, 
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="DeleteBusinessFailed",
            message="An unexpected error occurred while delete Business.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
        
@router.get(
    "/all-businesses/",
    response_model=List[BusinessResponse],
    summary="Get all Businesses for the current user",
    response_description="A list of the user's businesses",
    status_code=status.HTTP_200_OK
)
async def get_all_businesses(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) -> List[BusinessResponse]:
    """
    Endpoint to retrieve all businesses associated with the authenticated user.

    Args:
        db (Session): SQLAlchemy database session dependency.
        user_id (str): ID of the authenticated user (from token).

    Returns:
        List[BusinessResponse]: A list of the user's businesses. An empty list is
        returned if the user has no businesses.
    """
    try:
        return get_all_businesses_by_user_service(
            user_id=user_id,
            db=db
        )
    except Exception as ex:
        # Re-lanzar excepciones conocidas o manejar las inesperadas
        if isinstance(ex, HTTPException):
            raise ex
        raise_app_error(
            error_code="GetAllBusinessesFailed",
            message="An unexpected error occurred while getting the businesses.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )