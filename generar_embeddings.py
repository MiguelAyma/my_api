import os
import json
import datetime
import time

import google.generativeai as genai
from dotenv import load_dotenv

# --- Imports de SQLAlchemy ---
from sqlalchemy import create_engine, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, declarative_base
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from app.data._db_config import get_db
from app.models.sql_alchemy_models import KnowledgeEntries


# --- Cargar variables de entorno ---
load_dotenv()

# --- Configuración de Gemini API ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la API Key de Gemini")
genai.configure(api_key=api_key)
embedding_model = "models/embedding-001"



# --- SCRIPT PRINCIPAL ---
def generate_and_save_embeddings():

    print("Iniciando proceso de generación de embeddings...")
    
    db_session_generator = get_db()
    db = next(db_session_generator) # Obtenemos la sesión del generador

    try:
        print("Paso 1: Obteniendo datos desde la base de datos...")
        # Usamos el ORM de SQLAlchemy para consultar los datos
        entries = db.query(KnowledgeEntries).all()

        if not entries:
            print("No se encontraron entradas en la base de datos.")
            return

        print(f"Se encontraron {len(entries)} entradas. Procesando...")
        
        all_embeddings = {}

        for entry in entries:
            # Combinamos título y contenido para un embedding más rico en contexto
            text_to_embed = f"Título: {entry.title}\nContenido: {entry.content}"
            
            print(f"  -> Procesando entry_id: {entry.entry_id}")
            
            try:
                # Paso 2: Generar el embedding con Gemini
                result = genai.embed_content(
                    model=embedding_model,
                    content=text_to_embed,
                    task_type="RETRIEVAL_DOCUMENT"
                )
                
                # Usamos el entry_id como clave en el diccionario (convertido a string)
                all_embeddings[str(entry.entry_id)] = result['embedding']

            except Exception as e:
                print(f"    ERROR al procesar la entrada {entry.entry_id}: {e}")

        # Paso 3: Guardar los embeddings en un archivo JSON local
        output_filename = 'embeddings_locales.json'
        print(f"\nProceso completado. Guardando {len(all_embeddings)} embeddings en '{output_filename}'...")
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(all_embeddings, f, indent=4)
            
        print("¡Guardado exitoso!")

    finally:
        # Nos aseguramos de cerrar la sesión que abrimos
        if db:
            db.close()


if __name__ == "__main__":
    generate_and_save_embeddings()