from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from routers.mates import mates_routers
from routers.auth import auth_routers
from routers.proveedor import proveedor_routers

app = FastAPI(
    title="API de amatear"
)

app.include_router(mates_routers, tags=["Mates"], prefix="/mates")
app.include_router(proveedor_routers, tags=["Proveedor"], prefix="/proveedor")
app.include_router(auth_routers, tags=["Autenticación"], prefix="/auth")
add_pagination(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#/configuro qué aplicaciones pueden comunicarse con mi API y qué operaciones tienen permitida

 