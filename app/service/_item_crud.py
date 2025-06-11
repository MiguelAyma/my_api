from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.sql_alchemy_models import Item 
from app.data._item_crud import create_item_data, delete_item_data,update_item_data,get_item_data, create_item_categories
from app.schemas._item import ItemBase, ItemNotFoundError, ItemResponse, DeleteItemResponse
from app.schemas._error import ErrorType, raise_app_error


def generate_item_slug(name: str, user_id: str, business_id: int) -> str:
    """
    Genera un slug a partir de un nombre

    Args:
        name: Nombre del ítem
        user_id: ID del usuario
        business_id: ID del negocio

    Returns:
        Slug generado
    """
    slug = name.lower().replace(" ", "-")
    user_prefix = user_id[:4]  # Tomar los primeros 4 caracteres del user_id
    return f"{slug}-{user_prefix}_{business_id}"

def create_item_service(
        user_id: str,
        item_create: ItemBase,
        db:Session
    ) -> ItemResponse:

    try:
        item_slug_generated=generate_item_slug(item_create.item_name,user_id,item_create.business_id)
        db_Item = Item(
            item_slug = item_slug_generated,
            business_id = item_create.business_id,
            item_name = item_create.item_name,
            item_description=item_create.item_description,
            price=item_create.price,
            price_discount=item_create.price_discount,
            is_visible=item_create.is_visible,
        )
       

        record: Item = create_item_data(db_Item, db)
        item_categories=create_item_categories(item_create.categories, record.item_id, db)
        
        return ItemResponse(
            business_id=record.business_id,
            item_slug=record.item_slug,
            item_id=record.item_id,
            item_name = record.item_name,
            item_description = record.item_description,
            price = record.price,
            price_discount = record.price_discount,
            is_visible = record.is_visible,
            categories=item_categories,
            created_at = record.created_at,
            updated_at = record.updated_at
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="ItemServiceError",
            message="Failed to create Item in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )

def update_item_service(
    item_update: ItemBase,
    item_id: int,
    db: Session
) -> ItemResponse:
    try:
        record: Item = update_item_data(
            db=db,
            item_data=item_update,
            item_id=item_id
        )

        return ItemResponse(
            business_id=record.business_id,
            item_slug=record.item_slug,
            item_id=record.item_id,
            item_name=record.item_name,
            item_description=record.item_description,
            price=record.price,
            price_discount=record.price_discount,
            is_visible=record.is_visible,
            categories=[ic.category_id for ic in record.categories],  # ← Extrae los IDs
            created_at=record.created_at,
            updated_at=record.updated_at
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="ItemServiceError",
            message="Failed to update Item in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )


def get_item_service(db: Session, business_id: int) -> List[ItemResponse]:
    """
    Obtiene todos los items de un negocio con sus categorías en formato Pydantic.
    
    Args:
        db (Session): Sesión de la base de datos.
        business_id (int): ID del negocio.
    
    Returns:
        List[ItemResponse]: Lista de items con sus categorías.
    
    Raises:
        HTTPException: Si no se encuentran items.
        AppError: Si ocurre un error inesperado.
    """
    try:
        items = get_item_data(business_id, db)
        
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No items found for business with ID {business_id}"
            )
        
        # Pre-procesar las categorías para evitar accesos a BD adicionales
        items_with_categories = []
        for item in items:
            category_ids = [ic.category.category_id for ic in item.categories]
            item_response = ItemResponse(
                business_id=item.business_id,
                item_id=item.item_id,
                item_slug=item.item_slug,
                item_name=item.item_name,
                item_description=item.item_description,
                price=float(item.price) if item.price else None,
                price_discount=float(item.price_discount) if item.price_discount else None,
                is_visible=item.is_visible,
                categories=category_ids,  # Solo enviamos los IDs
                created_at=item.created_at,
                updated_at=item.updated_at
            )
            items_with_categories.append(item_response)
        
        return items_with_categories
        
    except HTTPException:
        raise
    except Exception as e:

        raise_app_error(
            error_code="ITEM_SERVICE_ERROR",
            message="Failed to retrieve items",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )
def delete_item_service(
        item_id: int,
        db: Session,

    ) -> DeleteItemResponse:
    """
    Delete a ACTIVITY item from the database.

    Args:
        ACTIVITY_id (str): The ID of the ACTIVITY item to delete.
        db (Session): The database session.
    """
    try:
        response = delete_item_data(item_id, db)
        return response
        
    except ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise_app_error(
            error_code="ItemServiceError",
            message="Failed to delete Item in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )