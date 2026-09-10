from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.mates import mates_routers

from database import Base, engine
from models.mate import Mate
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de amatear"
)

app.include_router(mates_routers, tags=["Mates"], prefix="/mates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#/configuro qué aplicaciones pueden comunicarse con mi API y qué operaciones tienen permitida

 