from fastapi import HTTPException

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
#from app.data._sqlalchemy_models import business
from app.models.sql_alchemy_models import Business
from app.schemas._business import BusinessBase, BusinessResponse
from app.schemas._error import ErrorType, raise_app_error #, BusinessNotFoundError, DeleteBusinessResponse


def create_business_data(db_business: Business, db: Session) -> Business:
    """CREATE Business

    Args:
        db_business (business): business db model
        db (Session): database dependency

    Raises:
        HTTPException: If a sql operation present errors

    Returns:
        business: business db model with data after inserting
    """
    try:
        db.add(db_business)
        db.commit()
        # db.refresh(db_Business)

        return db_business
    except SQLAlchemyError as e:
        db.rollback()
        raise_app_error(
            error_code="DatabaseBusinessError",
            message="Failed to insert the new Business into the database.",
            error_type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "insert",
                "model": "business"
            }
        )
        
def update_business_data(
        user_id: str,
        business_id: int,
        business_data: BusinessBase,
        db: Session
    ) -> Business:
    """Update an existing Business in the database.

    Args:
        user_id (str): The ID of the user who owns the Business.
        Business_id (int): The ID of the Business to be updated.
        Business_data (BusinessBase): The new data for the Business.
        db (Session): The database session.

    Raises:
        HTTPException: If the Business is not found or a SQL operation presents errors.

    Returns:
        Business: The updated Business database model instance.
    """
    try:

        db_business = db.query(Business).filter(
            Business.business_id == business_id,
            Business.user_id == user_id
        ).first()

        if db_business is None:
            raise HTTPException(
                status_code=404,
                detail='Business not found'
            )
        update_data = business_data.model_dump(exclude_unset=True)
        # Check if the Business is linked to a habit

            
        for key, value in update_data.items():
            setattr(db_business, key, value)

        db.commit()
        return db_business
    except SQLAlchemyError as e:
        # Rollback the transaction in case of error
        db.rollback()
        # Log the exception for debugging purposes
        print(f"DB Error updating Business item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise_app_error(
            error="DatabaseBusinessError",
            message="Failed to update Business into the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "update",
                "model": "Business"
            }
        )
        
def get_business_data(user_id: str,business_id:int ,db: Session) -> Business:

    try:
        db_business = db.query(Business).filter(           
            Business.business_id == business_id,
            Business.user_id == user_id).first()
        if db_business is None:
            raise HTTPException(
                    status_code=404,
                    detail='Business not found'
                )
        return  db_business
    except SQLAlchemyError as e:
        raise_app_error(
            error="DatabaseBusinessError",
            message="Failed to get Business from the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "get",
                "model": "Business"
            }
        )