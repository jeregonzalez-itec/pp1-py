from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from src.models.mate import Mate, MateBase

router = APIRouter(
    prefix="/mates",
    tags=["Mates"]
)

mates_db = [
    {
        "id": 1,
        "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-26-at-15-43-36-15bb01a41683c6b0fa17798993102248-1024-1024.webp",
        "nombre": "Mate Imperial",
        "material": "Cuero",
        "precio": 25000,
        "stock": 5
    },
    {
        "id": 2,
        "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-26-at-15-43-43-80291fa244c7918b1717798986879104-1024-1024.webp",
        "nombre": "Mate Camionero",
        "material": "Calabaza",
        "precio": 18000,
        "stock": 10
    },
    {
        "id": 3,
        "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-12-at-14-38-58-1-f46bd7a41c5701bff617786537846413-1024-1024.webp",
        "nombre": "IMPERIAL CRIOLLO DE CALABAZA",
        "material": "Calabaza",
        "precio": 40000,
        "stock": 3
    },
    {
        "id": 4,
        "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/whatsapp-image-2026-05-26-at-15-43-35-3-abf4f884bb4d17e11817798221302116-1024-1024.webp",
        "nombre": "Mate galleta",
        "material": "Calabaza",
        "precio": 20000,
        "stock": 6
    },
    {
        "id": 5,
        "image": "https://dcdn-us.mitiendanube.com/stores/007/657/161/products/metalico-87d5ab8228c9808e4717779946991298-1024-1024.webp",
        "nombre": "Mate Termico",
        "material": "Acero Inoxidable",
        "precio": 10000,
        "stock": 9
    },
] 


@router.get("/", response_model=list[Mate])
def obtener_mates():
    return mates_db


@router.get(
    "/{mate_id}",
    response_model=Mate,
    responses={404: {"description": "Mate no encontrado"}}
)
def obtener_mate_por_id(
    mate_id: Annotated[
        int,
        Path(description="ID del mate")
    ]
):
    for mate in mates_db:
        if mate["id"] == mate_id:
            return mate

    raise HTTPException(
        status_code=404,
        detail="Mate no encontrado"
    )


@router.post("/", response_model=Mate)
def crear_mate(mate: MateBase):

    nuevo_mate = {
        "id": len(mates_db) + 1,
        **mate.model_dump()
    }

    mates_db.append(nuevo_mate)

    return nuevo_mate


@router.put(
    "/{mate_id}",
    response_model=Mate,
    responses={404: {"description": "Mate no encontrado"}}
)
def actualizar_mate(
    mate_id: Annotated[
        int,
        Path(description="ID del mate")
    ],
    mate_actualizado: MateBase
):

    for indice, mate in enumerate(mates_db):

        if mate["id"] == mate_id:

            mates_db[indice] = {
                "id": mate_id,
                **mate_actualizado.model_dump()
            }

            return mates_db[indice]

    raise HTTPException(
        status_code=404,
        detail="Mate no encontrado"
    )


@router.delete(
    "/{mate_id}",
    response_model=Mate,
    responses={404: {"description": "Mate no encontrado"}}
)
def eliminar_mate(
    mate_id: Annotated[
        int,
        Path(description="ID del mate")
    ]
):

    for indice, mate in enumerate(mates_db):

        if mate["id"] == mate_id:

            eliminado = mates_db.pop(indice)

            return eliminado

    raise HTTPException(
        status_code=404,
        detail="Mate no encontrado"
    )