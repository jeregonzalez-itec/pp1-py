from typing import Any

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session


def not_found_response(label: str) -> dict[int, dict[str, Any]]:
    """Documenta en /docs el error 404 que levantan los endpoints que buscan por id."""
    return {
        404: {
            "description": f"{label} no encontrado",
            "content": {
                "application/json": {"example": {"detail": f"{label} no encontrado"}}
            },
        }
    }


CONFLICT_RESPONSE: dict[int, dict[str, Any]] = {
    409: {
        "description": "Conflicto: valor duplicado o registro con dependencias",
        "content": {
            "application/json": {
                "example": {"detail": "Ya existe un registro con esos datos únicos"}
            }
        },
    }
}


def get_or_404(db: Session, model: type, id: int, label: str):
    """Busca por id; si no existe levanta HTTPException 404."""
    obj = db.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{label} no encontrado")
    return obj


def commit_or_409(db: Session) -> None:
    """Hace commit; si se viola un UNIQUE devuelve 409 en vez de un 500."""
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Ya existe un registro con esos datos únicos"
        )
