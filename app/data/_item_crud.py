from typing import List
from fastapi import HTTPException

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_alchemy_models import Item, Category, ItemCategory
from app.schemas._item import ItemBase, ItemNotFoundError, ItemResponse, DeleteItemResponse
from app.schemas._error import ErrorType, raise_app_error #, ItemNotFoundError, DeleteItemResponse
from sqlalchemy.orm import joinedload


def create_item_data(db_item: Item, db: Session) -> Item:
    """CREATE Item

    Args:
        db_item (Item): Item db model
        db (Session): database dependency

    Raises:
        HTTPException: If a sql operation present errors

    Returns:
        Item: Item db model with data after inserting
    """
    try:
        db.add(db_item)
        db.commit()
        # db.refresh(db_item)

        return db_item
    except SQLAlchemyError as e:
        db.rollback()
        raise_app_error(
            error_code="DatabaseItemError",
            message="Failed to insert the new Item into the database.",
            error_type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "insert",
                "model": "Item"
            }
        )
        
def create_item_categories(
    category_ids: List[int], 
    item_id: int, 
    db: Session
) -> List[int]:
    """
    Crea relaciones entre un item y múltiples categorías en la tabla ItemCategory.
    
    Args:
        category_ids (List[int]): Lista de IDs de categorías a relacionar con el item.
        item_id (int): ID del item al que se asociarán las categorías.
        db (Session): Sesión de la base de datos.
    
    Returns:
        List[int]: Lista de IDs de categorías que fueron insertadas correctamente.
    
    Raises:
        HTTPException: Si ocurre un error de validación o no se encuentran categorías.
        AppError: Si ocurre un error inesperado durante la operación.
    """
    try:
        # Validar que recibimos datos
        if not category_ids:
            raise HTTPException(
                status_code=400,
                detail="No category IDs provided"
            )
        
        # Verificar que las categorías existan
        existing_categories = db.query(Category.category_id).filter(
            Category.category_id.in_(category_ids)
        ).all()
        
        existing_category_ids = {cat.category_id for cat in existing_categories}
        missing_ids = set(category_ids) - existing_category_ids
        
        if missing_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Categories not found: {missing_ids}"
            )
        
        # Crear las relaciones ItemCategory
        new_relations = []
        for category_id in category_ids:
            item_category = ItemCategory(
                item_id=item_id,
                category_id=category_id
            )
            db.add(item_category)
            new_relations.append(category_id)
        
        db.commit()
        
        return new_relations
        
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise_app_error(
            error_code="ITEM_CATEGORY_CREATION_ERROR",
            message="Database error while creating item-category relationships",
            error_type=ErrorType.DATA,
            details=str(e)
        )
    except Exception as e:
        db.rollback()
        raise_app_error(
            error_code="ITEM_CATEGORY_SERVICE_ERROR",
            message="Unexpected error creating item categories",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )
        
def update_item_data(
    item_id: int,
    item_data: ItemBase,
    db: Session
) -> Item:
    try:
        db_item = db.query(Item).filter(Item.item_id == item_id).first()

        if db_item is None:
            raise HTTPException(status_code=404, detail='Item not found')

        update_data = item_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key != "categories":  # No actualices categorías aquí
                setattr(db_item, key, value)

        # Sincroniza las relaciones con categorías
        if "categories" in update_data:
            new_category_ids = set(update_data["categories"])
            current_category_ids = {ic.category_id for ic in db_item.categories}

            for ic in db_item.categories[:]:  # copia segura
                if ic.category_id not in new_category_ids:
                    db.delete(ic)

            # Agrega nuevas relaciones
            for category_id in new_category_ids - current_category_ids:
                db.add(ItemCategory(item_id=item_id, category_id=category_id))

        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        # Rollback the Item in case of error
        db.rollback()
        # Log the exception for debugging purposes
        print(f"DB Error updating Item item: {e}")
        # Re-raise the exception to be handled at a higher level
        raise_app_error(
            error="DatabaseItemError",
            message="Failed to update Item into the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "update",
                "model": "Item"
            }
        )
        
def get_item_data(business_id: int, db: Session) -> List[Item]:
    """
    Obtiene todos los items de un negocio con sus categorías relacionadas en una sola consulta eficiente.
    
    Args:
        business_id (int): ID del negocio
        db (Session): Sesión de la base de datos
    
    Returns:
        List[Item]: Lista de items con sus categorías cargadas
    """
    try:
        return db.query(Item)\
            .options(joinedload(Item.categories).joinedload(ItemCategory.category))\
            .filter(Item.business_id == business_id)\
            .order_by(Item.item_id)\
            .all()
    except SQLAlchemyError as e:
        raise_app_error(
            error="DatabaseItemError",
            message="Failed to get Item from the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "get",
                "model": "Item"
            }
        )
        
def delete_item_data(item_id: int, db: Session) -> DeleteItemResponse:
    """
    Delete an existing ACTIVITY item from the database.

    Args:
        activity_id (str): The ID of the ACTIVITY item to delete.
        db (Session): The database session.
    """
    try:
        db_item = db.query(Item).filter(
            Item.item_id == item_id
        ).first()
        if not db_item :
            raise ItemNotFoundError(f"Item with id {item_id} not found")

        db.delete(db_item)
        db.commit()
        return DeleteItemResponse(
            message="Resource deleted successfully",
            id=item_id
        )

    except SQLAlchemyError as e:
        # Rollback the Item in case of error
        db.rollback()
        raise_app_error(
            error="DatabaseItemError",
            message="Failed to delete Item into the database.",
            type=ErrorType.DATA,
            status_code=500,
            details=str(e),
            additional_data={
                "operation": "delete",
                "model": "Item"
            }
        )