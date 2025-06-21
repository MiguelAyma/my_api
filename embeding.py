import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict

# --- Configuración Inicial ---
# Asegúrate de que esto se ejecute al inicio de tu aplicación
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY.")
genai.configure(api_key=api_key)

# --- Constantes ---
# Es una buena práctica definir el modelo y el nombre del archivo en un solo lugar
EMBEDDING_MODEL = 'models/text-embedding-004' # Modelo recomendado para tareas de RAG
EMBEDDINGS_FILE = 'embeddings_locales_test.json'

def add_embedding_to_store(entry_id: int, improved_title: str, improved_content: str):
    """
    Genera un embedding para una única entrada y lo añade al almacén JSON.
    Si el archivo no existe, lo crea.
    """
    print(f"-> Iniciando la generación de embedding para la entrada ID: {entry_id}")

    # 1. Cargar el almacén de embeddings existente o crear uno nuevo
    embeddings_store: Dict[str, list] = {}
    try:
        if os.path.exists(EMBEDDINGS_FILE):
            with open(EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
                embeddings_store = json.load(f)
            print(f"-> Almacén de embeddings '{EMBEDDINGS_FILE}' cargado con {len(embeddings_store)} entradas.")
        else:
            print(f"-> No se encontró '{EMBEDDINGS_FILE}'. Se creará un nuevo archivo.")
            
    except json.JSONDecodeError:
        print(f"-> ADVERTENCIA: El archivo '{EMBEDDINGS_FILE}' está corrupto o vacío. Se creará uno nuevo.")
    
    # 2. Preparar el texto para generar el embedding
    # Usamos el contenido mejorado para obtener el mejor contexto semántico
    text_to_embed = f"Título: {improved_title}\nContenido: {improved_content}"

    # 3. Generar el embedding con la API de Gemini
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text_to_embed,
            task_type="RETRIEVAL_DOCUMENT" # Tarea optimizada para búsqueda (RAG)
        )
        new_embedding = result['embedding']
        print(f"-> Embedding generado exitosamente para la entrada ID: {entry_id}")
    except Exception as e:
        print(f"ERROR: No se pudo generar el embedding para la entrada {entry_id}. Error: {e}")
        # Decidimos no continuar si la API de embedding falla.
        return

    # 4. Añadir el nuevo embedding al diccionario (usando el ID como clave string)
    embeddings_store[str(entry_id)] = new_embedding

    # 5. Guardar el diccionario actualizado de vuelta en el archivo JSON
    try:
        with open(EMBEDDINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(embeddings_store, f, indent=4)
        print(f"-> Embedding para la entrada {entry_id} guardado. El almacén ahora tiene {len(embeddings_store)} entradas.")
    except Exception as e:
        print(f"ERROR: No se pudo guardar el archivo de embeddings '{EMBEDDINGS_FILE}'. Error: {e}")

