from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from routers.auth import auth_routers
from routers.mascota import mascota_routers
from routers.tagnfc import tagnfc_routers
from routers.usuario import usuario_routers
from routers.veterinaria import veterinaria_routers

app = FastAPI(
    title="API Veterinaria NFC",
    description=(
        "API REST para gestionar veterinarias, tags NFC/QR, mascotas y sus dueños. "
        "Cada mascota se identifica mediante un tag NFC emitido por una veterinaria. "
        "Incluye autenticación con JWT, paginación y migraciones con Alembic."
    ),
    version="1.0.0",
)

# CORS: qué orígenes (la EFI de JavaScript) pueden consumir la API.
# OJO: los orígenes van SIN barra final.
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(veterinaria_routers, prefix="/veterinarias", tags=["Veterinarias"])
app.include_router(tagnfc_routers, prefix="/tags", tags=["Tags NFC"])
app.include_router(mascota_routers, prefix="/mascotas", tags=["Mascotas"])
app.include_router(usuario_routers, prefix="/usuarios", tags=["Usuarios"])
app.include_router(auth_routers, prefix="/auth", tags=["Autenticación"])

# Paginación (fastapi-pagination): habilita Page[...] en los get all
add_pagination(app)
