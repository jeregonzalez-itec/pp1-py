from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.mates import router as mates_router
#/Esto importa todos los endpoints que hice en src/routers/mates.py
app = FastAPI(
    title="API de amatear"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#/configuro qué aplicaciones pueden comunicarse con mi API y qué operaciones tienen permitida

app.include_router(mates_router)
