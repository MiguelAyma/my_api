from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from core.config import settings  # Archivo donde centralizas la configuración (e.g., ALLOW_ORIGINS)
from app.core.config import settings
from app.routers import (
    user
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="My API",
    version="1.0.0",
)
# Servir archivos estáticos desde la carpeta "media"
#app.mount("/media", StaticFiles(directory="media"), name="media")
# Configuración de CORS (puedes ajustar los orígenes permitidos en core/config.py)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz
@app.get("/")
def read_root():
    return {"Hello": "World _"}

# Registro de routers con versionado en la URL
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])















