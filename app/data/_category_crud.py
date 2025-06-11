from typing import List
from fastapi import HTTPException


from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_alchemy_models import Category
from app.schemas._category import CategoryBase, CategoryNotFoundError, DeleteCategoryResponse
from app.schemas._error import ErrorType, raise_app_error #, CategoryNotFoundError, DeleteCategoryResponse


def create_category_data(db_category: Category, db: Session) -> Category:
    """CREATE Category

    Args:
        db_Category (Category): Category db model
        db (Session): database dependency

    Raises:
        HTTPException: If a sql operation present errors

    Returns:
        Category: Category db model with data after inserting
    """
    try:
        db.add(db_category)
        db.commit()
        # db.refresh(db_Category)

        return db_category
    except SQLAlchemyError as e:
        db.rollback()
        raise_app_error(
            error_code="DatabaseCategoryError",
            message="Failed to insert the new Category into the database.",
            error_type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "insert",
                "model": "Category"
            }
        )
        
def update_category_data(
        category_id: int,
        category_data: CategoryBase,
        db: Session
    ) -> Category:
    """Update an existing Category in the database.

    Args:
        user_id (str): The ID of the user who owns the Category.
        Category_id (int): The ID of the Category to be updated.
        Category_data (CategoryBase): The new data for the Category.
        db (Session): The database session.

    Raises:
        HTTPException: If the Category is not found or a SQL operation presents errors.

    Returns:
        Category: The updated Category database model instance.
    """
    try:

        db_category = db.query(Category).filter(
            Category.category_id == category_id,
            #Category.business_id == business_id
        ).first()

        if db_category is None:
            raise HTTPException(
                status_code=404,
                detail='Category not found'
            )
        update_data = category_data.model_dump(exclude_unset=True)
        # Check if the Category is linked to a habit

            
        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        return db_category
    except SQLAlchemyError as e:
        # Rollback the Category in case of error
        db.rollback()
        # Log the exception for debugging purposes
        print(f"DB Error updating Category item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise_app_error(
            error="DatabaseCategoryError",
            message="Failed to update Category into the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "update",
                "model": "Category"
            }
        )
        
def get_category_data(business_id:int ,db: Session) -> List[Category]:

    try:
        db_categories = db.query(Category).filter(           
            Category.business_id == business_id,
            Category.is_active == True
        ).all()
        if db_categories is None:
            raise HTTPException(
                    status_code=404,
                    detail='Categories not found'
                )
        return  db_categories
    except SQLAlchemyError as e:
        raise_app_error(
            error="DatabaseCategoryError",
            message="Failed to get Category from the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "get",
                "model": "Category"
            }
        )
        
def delete_category_data(category_id: int, db: Session) -> DeleteCategoryResponse:
    """
    Delete an existing ACTIVITY item from the database.

    Args:
        activity_id (str): The ID of the ACTIVITY item to delete.
        db (Session): The database session.
    """
    try:
        db_category = db.query(Category).filter(
            Category.category_id == category_id  
        ).first()
        if not db_category :
            raise CategoryNotFoundError(f"Category with id {category_id} not found")

        db_category.is_active = False  # Marcamos como inactivo
        db.commit()
        db.refresh(db_category)  #actualizar el objeto en memoria
        return DeleteCategoryResponse(
            message="Resource deleted successfully",
            id=category_id
        )

    except SQLAlchemyError as e:
        # Rollback the Category in case of error
        db.rollback()
        raise_app_error(
            error="DatabaseCategoryError",
            message="Failed to delete Category into the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "delete",
                "model": "Category"
            }
        )
        
def count_categories_by_business_id(business_id: str, db: Session) -> int:
    """Cuenta cuántas categorías existen para un business_id."""
    try:
        return db.query(Category).filter(Category.business_id == business_id).count()
    except SQLAlchemyError as e:
        raise_app_error(
            error_code="CountCategoryError",
            message="Error al contar las categorías por business_id.",
            error_type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={"operation": "count", "business_id": business_id}
        )
