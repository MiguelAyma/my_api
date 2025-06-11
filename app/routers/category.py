
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, Header, Query
from sqlalchemy.orm import Session
from app.schemas._error import ErrorType, raise_app_error
from app.data._db_config import get_db
from utils._user_validation import get_current_user
from app.schemas._category import CategoryBase, CategoryResponse, DeleteCategoryResponse
from app.service._category_crud import create_category_service, delete_category_service, update_category_service, get_category_service




router = APIRouter()

@router.post("/", response_model=CategoryResponse)
async def insert_category(
    category: CategoryBase,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user), 
) -> CategoryResponse:

    try :
        return create_category_service(
            category_create = category,
            db = db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="CreateCategoryFailed",
            message="An unexpected error occurred while creating the category.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update an existing Category",
    response_description="The updated Category",
    status_code=status.HTTP_200_OK
)
async def update_Category(
    category_id: int,
    category_update: CategoryBase,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) -> CategoryResponse:
    """
    Endpoint to update an existing Category by its ID.

    Args:
        Category_id (int): ID of the Category to update.
        Category_update (CategoryBase): New data to update the Category.
        db (Session): SQLAlchemy database session dependency.
        user_id (str): ID of the authenticated user (extracted from the token).

    Returns:
        CategoryResponse: The updated Category data.

    Raises:
        HTTPException:
            - 404: If the Category is not found or doesn't belong to the user.
            - 500: If an unexpected error occurs.
    """
    try:
        return update_category_service(
            category_update=category_update,
            category_id=category_id,
            db=db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="UpdateCategoryFailed",
            message="An unexpected error occurred while updating the Category.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )
        
@router.get(
    "/",
    response_model=List[CategoryResponse],
    summary="get an existing Category",
    response_description="Get Category",
    status_code=status.HTTP_200_OK
)
async def get_Category(
    business_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) -> List[CategoryResponse]:
    """
    Endpoint to update an existing Category by its ID.

    Args:
        Category_id (int): ID of the Category to update.
        Category_update (CategoryBase): New data to update the Category.
        db (Session): SQLAlchemy database session dependency.
        user_id (str): ID of the authenticated user (extracted from the token).

    Returns:
        CategoryResponse: The updated Category data.

    Raises:
        HTTPException:
            - 404: If the Category is not found or doesn't belong to the user.
            - 500: If an unexpected error occurs.
    """
    try:
        return get_category_service(
            business_id=business_id,
            db=db
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="getCategoryFailed",
            message="An unexpected error occurred while get the Category.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Category",
    response_model=DeleteCategoryResponse
)
def delete_Category(
        category_id: int,
        db: Session = Depends(get_db),
        user_id: str = Depends(get_current_user)
    ):
    """
    Delete a Single ACTIVITY item

    Args:
        todo_id (UUID): TODO ID
        db (Session, optional):  Dependency Injection
        user_id (UUID, optional):  Dependency Injection

    Returns:
        null
    """
    try:

        return delete_category_service(
            category_id, 
            db, 
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise_app_error(
            error_code="DeleteCategoryFailed",
            message="An unexpected error occurred while delete Category.",
            error_type=ErrorType.HANDLER,
            details=str(ex)
        )

