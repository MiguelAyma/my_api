from sqlalchemy.orm import Session
from app.schemas._error import ErrorType, raise_app_error
from app.schemas._knowledge_entry import KnowledgeEntryCreate, KnowledgeEntryDBModel, KnowledgeEntryUpdate, KnowledgeEntryResponse, KnowledgeEntryImproved
from app.data._knowledge_entry_crud import create_knowledge_entry, update_knowledge_entry
from app.utils.agent_improved import create_enhanced_entry_agent
from embeding import add_embedding_to_store

def create_knowledge_entry_service(db: Session, data: KnowledgeEntryCreate) -> KnowledgeEntryImproved:
    """
    Servicio para crear una nueva entrada, enriqueciéndola primero con el agente de IA.
    """
    print("Recibida nueva entrada. Enviando al agente de IA para mejorarla...")
    try:
        # 1. Llamamos al agente con los datos de entrada
        enhanced_data = create_enhanced_entry_agent(data.title, data.content)

        # 2. Preparamos el objeto completo para la base de datos
        new_data_for_db = KnowledgeEntryDBModel(
            business_id=data.business_id,  # Original
            title=data.title,               # Original
            content=data.content,           # Original
            content_type=data.content_type, # Original
            improved_title=enhanced_data.improved_title, # Mejorado por la IA
            improved_content=enhanced_data.improved_content, # Mejorado por la IA
            icon=enhanced_data.icon,                         # Elegido por la IA
            categories=enhanced_data.categories              # Generado por la IA
        )

        # 3. Llamamos a la función que interactúa con la BD
        entry = create_knowledge_entry(db, new_data_for_db)

        # 4. Validamos y devolvemos el modelo de respuesta final
        return KnowledgeEntryImproved.model_validate(entry)

    except Exception as e:
        raise_app_error(
            error_code="EntryServiceError",
            message="Failed to create Entry in service layer.",
            error_type=ErrorType.SERVICE,
            details=str(e)
        )

def create_knowledge_entry_service2(db: Session, data: KnowledgeEntryCreate) -> KnowledgeEntryImproved:
    """
    Servicio para crear una nueva entrada, enriqueciéndola con el agente de IA
    y generando su embedding de forma inmediata.
    """
    print("Recibida nueva entrada. Enviando al agente de IA para mejorarla...")
    try:
        # 1. Llamamos al agente de IA para mejorar el título y contenido
        enhanced_data = create_enhanced_entry_agent(data.title, data.content)

        # 2. Preparamos el objeto completo para la base de datos
        new_data_for_db = KnowledgeEntryDBModel(
            business_id=data.business_id,
            title=data.title,
            content=data.content,
            content_type=data.content_type,
            improved_title=enhanced_data.improved_title,
            improved_content=enhanced_data.improved_content,
            icon=enhanced_data.icon,
            categories=enhanced_data.categories
        )

        # 3. Guardamos la entrada en la base de datos para obtener su ID
        entry = create_knowledge_entry(db, new_data_for_db)
        print(f"Entrada creada en la base de datos con ID: {entry.entry_id}")

        # 4. ¡NUEVO PASO! Generamos y guardamos el embedding para esta nueva entrada
        # Lo hacemos en un try/except para que un fallo aquí no impida la creación del entry
        try:
            add_embedding_to_store(
                entry_id=entry.entry_id,
                improved_title=entry.improved_title,
                improved_content=entry.improved_content
            )
        except Exception as e:
            # En una aplicación real, aquí podrías loggear este error específico
            # para regenerar el embedding más tarde.
            print(f"ADVERTENCIA: La entrada {entry.entry_id} se creó, pero falló la generación de su embedding: {e}")


        # 5. Validamos y devolvemos el modelo de respuesta final
        return KnowledgeEntryImproved.model_validate(entry)

    except Exception as e:
        # Tu manejador de errores existente
        raise_app_error(
            error_code="EntryServiceError",
            message="Failed to create Entry in service layer.",
            error_type="SERVICE", # Asumo que tienes un Enum o similar
            details=str(e)
        )

def update_knowledge_entry_service(db: Session, entry_id: int, data: KnowledgeEntryUpdate) -> KnowledgeEntryResponse:
    entry = update_knowledge_entry(db, entry_id, data)
    return KnowledgeEntryResponse.model_validate(entry)
