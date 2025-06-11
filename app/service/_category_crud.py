""" Service Category crud operation """

from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

#from app.data._sqlalchemy_models import Category
from app.models.sql_alchemy_models import Category 
from app.data._category_crud import count_categories_by_business_id, create_category_data, delete_category_data,update_category_data,get_category_data
from app.schemas._category import CategoryBase, CategoryNotFoundError, CategoryResponse, DeleteCategoryResponse
from app.schemas._error import ErrorType, raise_app_error
from app.utils.config import CATEGORY_LIMIT_PER_BUSINESS
def create_category_service(
    category_create: CategoryBase,
    db: Session
) -> CategoryResponse:
    try:
        count = count_categories_by_business_id(category_create.business_id, db)

        if count >= CATEGORY_LIMIT_PER_BUSINESS:
            raise_app_error(
                error_code="CategoryLimitExceeded",
                message=f"El negocio ya tiene el máximo de {CATEGORY_LIMIT_PER_BUSINESS} categorías permitidas.",
                error_type=ErrorType.VALIDATION,
                status_code=413,
                details=f"business_id: {category_create.business_id}",
                additional_data={"limit": CATEGORY_LIMIT_PER_BUSINESS}
            )

        db_category = Category(
            business_id=category_create.business_id,
            category_name=category_create.category_name,
            icon=category_create.icon,
        )

        record: Category = create_category_data(db_category, db)

        return CategoryResponse(
            business_id=record.business_id,
            category_id=record.category_id,
            category_name=record.category_name,
            icon=record.icon,
            created_at=record.created_at,
            updated_at=record.updated_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="CategoryServiceError",
            message="Failed to create Category in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )



def update_category_service(
    category_update: CategoryBase,
    category_id: int,
    db: Session
) -> CategoryResponse:
    """
    Update an existing Category and invalidate related cache if necessary.

    Args:
        Category_update (CategoryBase): Updated data for the Category.
        Category_id (int): ID of the Category to update.
        user_id (str): ID of the user who owns the Category.
        db (Session): SQLAlchemy database session.

    Returns:
        CategoryResponse: Data of the updated Category.

    Raises:
        HTTPException: If the Category does not exist or update fails.
    """
    try:
        db_category = CategoryBase(
            business_id=category_update.business_id,
            category_name = category_update.category_name,
            icon = category_update.icon,
        )
        record: Category = update_category_data(
            db=db,
            category_data=db_category,
            category_id=category_id
        )

        return CategoryResponse(
            business_id=record.business_id,
            category_id=record.category_id,
            category_name = record.category_name,
            icon = record.icon,
            created_at = record.created_at,
            updated_at = record.updated_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="CategoryServiceError",
            message="Failed to update Category in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )
def get_category_service(db: Session, business_id: int) -> List[CategoryResponse]:
    """
    Obtiene todas las categorías asociadas a un negocio específico.
    
    Args:
        db (Session): Sesión de la base de datos.
        business_id (int): ID del negocio para el cual se buscan las categorías.
    
    Returns:
        List[CategoryResponse]: Lista de categorías en formato Pydantic.
    
    Raises:
        HTTPException: Si no se encuentran categorías para el business_id proporcionado.
        AppError: Si ocurre un error inesperado durante el proceso.
    """
    try:
        categories: List[Category] = get_category_data(business_id, db)
        
        if not categories:
            raise HTTPException(
                status_code=404,
                detail=f"No categories found for business with ID {business_id}"
            )
        
        # Convertir todos los registros de SQLAlchemy a Pydantic
        return [
            CategoryResponse(
                business_id=category.business_id,
                category_id=category.category_id,
                category_name=category.category_name,
                icon=category.icon,
                created_at=category.created_at,
                updated_at=category.updated_at
            )
            for category in categories
        ]
        
    except HTTPException:
        # Re-lanzar las excepciones HTTP que ya manejamos
        raise
    except Exception as e:
        # Manejar otros errores inesperados
        raise_app_error(
            error_code="CATEGORY_SERVICE_ERROR",
            message="Failed to retrieve categories in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )
def delete_category_service(
        category_id: int,
        db: Session,

    ) -> DeleteCategoryResponse:
    """
    Delete a ACTIVITY item from the database.

    Args:
        ACTIVITY_id (str): The ID of the ACTIVITY item to delete.
        db (Session): The database session.
    """
    try:
        response = delete_category_data(category_id, db)
        return response
        
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="CategoryServiceError",
            message="Failed to delete Category in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )