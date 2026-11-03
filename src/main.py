import sys
from pathlib import Path
from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqlmodel import SQLModel

from database import engine
from routers.auth import auth_routers
from routers.usuario import usuario_routers
from routers.mascota import mascota_routers
from routers.tagnfc import tagnfc_routers
from routers.veterinaria import veterinaria_routers
from routers.scan import scan_routers


app = FastAPI(
    title="Encontrame API",
    description="Backend oficial de Encontrame: plataforma de identificación y reencuentro de mascotas con chapitas inteligentes NFC y QR.",
    version="1.1.0",
  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen en entorno de desarrollo/API pública NFC
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
app.include_router(scan_routers, prefix="/scan", tags=["Escaneo Público y Reclamo"])
app.include_router(auth_routers, prefix="/auth", tags=["Autenticación"])
app.include_router(usuario_routers, prefix="/usuarios", tags=["Usuarios"])
app.include_router(mascota_routers, prefix="/mascotas", tags=["Mascotas"])
app.include_router(tagnfc_routers, prefix="/tags", tags=["Tags NFC"])
app.include_router(veterinaria_routers, prefix="/veterinarias", tags=["Veterinarias"])

# Paginación
add_pagination(app)


@app.get("/", tags=["General"])
def root():
    return {
        "app": "Encontrame API",
        "status": "online",
        "version": "1.1.0",
        "docs": "/docs",
    }
