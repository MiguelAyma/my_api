import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
ITEM_LIMIT_PER_BUSINESS = int(os.getenv("ITEM_LIMIT_PER_BUSINESS"))

CATEGORY_LIMIT_PER_BUSINESS = int(os.getenv("CATEGORY_LIMIT_PER_BUSINESS"))

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



