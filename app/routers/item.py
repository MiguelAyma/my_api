from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, Header, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.schemas._error import ErrorType, raise_app_error

from app.data._db_config import get_db

from utils._user_validation import get_current_user
from app.schemas._item import ItemBase, ItemResponse, DeleteItemResponse
from app.service._item_crud import create_item_service, delete_item_service, update_item_service, get_item_service




router = APIRouter()

@router.post("/", response_model=ItemResponse)
async def insert_item(
    item: ItemBase,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user), 
) -> ItemResponse:

    try :
        return create_item_service(
            user_id = user_id,
            item_create = item,
            db = db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="CreateItemFailed",
            message="An unexpected error occurred while creating the Item.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
        
@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update an existing Item",
    response_description="The updated Item",
    status_code=status.HTTP_200_OK
)
async def update_item(
    item_id: int,
    item_update: ItemBase,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) -> ItemResponse:
    """
    Endpoint to update an existing Item by its ID.

    Args:
        Item_id (int): ID of the Item to update.
        Item_update (ItemBase): New data to update the Item.
        db (Session): SQLAlchemy database session dependency.
        user_id (str): ID of the authenticated user (extracted from the token).

    Returns:
        ItemResponse: The updated Item data.

    Raises:
        HTTPException:
            - 404: If the Item is not found or doesn't belong to the user.
            - 500: If an unexpected error occurs.
    """
    try:
        return update_item_service(
            item_update=item_update,
            item_id=item_id,
            db=db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="UpdateItemFailed",
            message="An unexpected error occurred while updating the Item.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
        
@router.get(
    "/",
    response_model=List[ItemResponse],
    summary="get an existing Item",
    response_description="Get Item",
    status_code=status.HTTP_200_OK
)
async def get_item(
    business_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) -> List[ItemResponse]:
    """
    Endpoint to update an existing Item by its ID.

    Args:
        Item_id (int): ID of the Item to update.
        Item_update (ItemBase): New data to update the Item.
        db (Session): SQLAlchemy database session dependency.
        user_id (str): ID of the authenticated user (extracted from the token).

    Returns:
        ItemResponse: The updated Item data.

    Raises:
        HTTPException:
            - 404: If the Item is not found or doesn't belong to the user.
            - 500: If an unexpected error occurs.
    """
    try:
        return get_item_service(
            business_id=business_id,
            db=db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="getItemFailed",
            message="An unexpected error occurred while get the Item.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )

@router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Item",
    response_model=DeleteItemResponse
)
def delete_Item(
        item_id: int,
        db: Session = Depends(get_db),
        user_id: str = Depends(get_current_user)
    ):
    """
    Delete a Single Item item

    Args:
        item_id (UUID): TODO ID
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        null
    """
    try:

        return delete_item_service(
            item_id, 
            db, 
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="DeleteItemFailed",
            message="An unexpected error occurred while delete Item.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
