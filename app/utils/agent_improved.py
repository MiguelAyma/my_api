import google.generativeai as genai

from app.schemas._knowledge_entry import ImprovedEntryData
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

# --- PASO CLAVE: Cargar las variables de entorno desde el archivo .env ---
# Esto debe ejecutarse antes de que intentes usar la variable de entorno.
load_dotenv()


# --- Lista de Íconos Disponibles ---
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY. Asegúrate de que tu archivo .env está configurado correctamente.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error al configurar la API de Gemini: {e}")
    # En una aplicación real, podrías querer detener la ejecución aquí.
    exit()

# Esta lista se la pasaremos al agente en el prompt.
AVAILABLE_ICONS =[     
    "ArrowLeftIcon",
    "ArrowUpIcon",
    "ArrowRightIcon",
    "ArrowDownIcon",
    "BrandLineIcon",
    "CodeIcon",
    "BookOpenIcon",
    "ChartBarIcon",
    "ChatBubbleIcon",
    "DocumentTextIcon",
    "HomeIcon",
    "LightBulbIcon",
    "UsersIcon",
    "CogIcon",
    "CheckIcon",
    "ChevronLeftIcon",
    "CircleCheckIcon",
    "ClipboardIcon",
    "DotsVerticalIcon",
    "DownloadIcon",
    "EyeIcon",
    "EyeOffIcon",
    "FacebookIcon",
    "FiltersIcon",
    "HorizontalLinesIcon",
    "InstagramIcon",
    "ListIcon",
    "MailIcon",
    "MapPinIcon",
    "PencilIcon",
    "PhotoIcon",
    "PlusIcon",
    "RefreshIcon",
    "ShoppingCartIcon",
    "TagIcon",
    "TikTokIcon",
    "TrashIcon",
    "WhatsappIcon",
    "XIcon",
    "ZoomIcon",
    "BuildindStoreIcon",
    "SparklesIcon",
    "CoffeeIcon",
    "ToolsKitchen3Icon",
    "HammerIcon",
    "MusicIcon",
    "ScissorsIcon",
    "DeviceLaptopIcon",
    "WreckingBallIcon",
    "PlaneIcon",
    "LeafIcon",
    "Gamepad2Icon",
    "StopwatchIcon",
    "FlowerIcon",
    "BrushIcon",
    "BrainIcon",
    "AlertTriangleIcon",
    "BoltIcon",
    "CardsIcon",
    "ExclamationCircleIcon",
    "LayoutGridIcon",
    "LockIcon",
    "StatsIcon",
    "ShirtIcon",
    "BookIcon",
    "CameraIcon",
    "CarIcon",
    "HeartIcon",
    "UmbrellaIcon",
    "PaletteIcon",
    "StethoscopeIcon",
    "CampFireIcon",
    "PizzaIcon",
    "BriefcaseIcon",
    "GiftIcon",
    "HeadphonesIcon",
    "CalendarIcon",
    "TruckIcon"
]

def create_enhanced_entry_agent(title: str, content: str) -> ImprovedEntryData:
    """
    Este es el agente de IA.
    Toma un título y contenido, y devuelve una estructura de datos mejorada.
    """
    # Configura el modelo de Gemini
    # Asegúrate de usar un modelo que soporte la salida estructurada, como gemini-2.5-flash
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        generation_config={"response_mime_type": "application/json"} # Forzamos la salida JSON
    )

    # Convertimos la lista de íconos a un string para el prompt
    icons_list_str = ", ".join(AVAILABLE_ICONS)

    # Creamos el prompt detallado para el modelo
    prompt = f"""
    Eres un experto editor de contenido y clasificador. Tu tarea es analizar el título y contenido proporcionados para mejorarlos y estructurarlos.

    Sigue estas instrucciones al pie de la letra:
    1.  **Mejora el Título**: Crea un nuevo título que sea más claro, descriptivo y atractivo que el original.
    2.  **Mejora el Contenido**: Reescribe o formatea el contenido para que sea más fácil de leer, corrigiendo errores gramaticales y mejorando la estructura. Puedes usar Markdown simple como negritas o listas si es necesario.
    3.  **Selecciona un Ícono**: De la siguiente lista de íconos disponibles, escoge UNO y solo UNO que mejor represente el tema del contenido: [{icons_list_str}].
    4.  **Genera Categorías con Emojis**: Basándote en el contenido, genera una lista de 2 a 5 categorías relevantes. Cada categoría DEBE tener el formato "emoji Nombre de Categoría". Por ejemplo: ["🤖 Tecnología", "💡 Productividad"].

    Título Original:
    "{title}"

    Contenido Original:
    "{content}"
    """

    # Hacemos la llamada al API pidiendo la salida estructurada
    # La librería se encargará de convertir el prompt y el esquema Pydantic
    # en la instrucción correcta para el modelo.
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
             response_schema=ImprovedEntryData, # ¡La magia sucede aquí!
        )
    )
    
    # La librería ya devuelve el objeto Pydantic parseado
    return ImprovedEntryData.model_validate_json(response.text)