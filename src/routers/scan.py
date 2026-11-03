from datetime import datetime, timezone
import urllib.parse
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from core.auth import get_current_user
from core.utils import commit_or_409
from database import get_db
from models.anidados import (
    ContactoDuenoPublic,
    PerfilMascotaScan,
    ReclamarTagRequest,
    TagScanResult,
)
from models.escaneo import EscaneoTag, ReporteAvistamientoCreate
from models.estadoMascota import EstadoMascotaEnum, EstadoTagEnum
from models.mascota import Mascota, MascotaPublic
from models.tagnfc import TagNFC
from models.usuario import Usuario

scan_routers = APIRouter()


def _buscar_tag_por_identificador(db: Session, identificador: str) -> TagNFC:
    """Busca el tag por token_publico, codigoQR o uidNFC."""
    query = select(TagNFC).where(
        (TagNFC.token_publico == identificador)
        | (TagNFC.codigoQR == identificador)
        | (TagNFC.uidNFC == identificador)
    )
    tag = db.exec(query).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag con identificador '{identificador}' no encontrado",
        )
    return tag


@scan_routers.get("/{identificador}", response_model=TagScanResult)
def escanear_tag(
    identificador: str,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Endpoint principal llamado al acercar el celular (NFC) o escanear el QR.
    - Si el tag es NUEVO/VIRGEN: Devuelve reclamado=False para guiar al usuario a registrarse y reclamarlo.
    - Si el tag YA ESTÁ CONFIGURADO: Devuelve el perfil público de la mascota con botón directo de contacto.
    """
    tag = _buscar_tag_por_identificador(db, identificador)

    # Caso 1: El tag aún no ha sido reclamado / no tiene mascota vinculada
    if not tag.mascota:
        return TagScanResult(
            reclamado=False,
            token_publico=tag.token_publico,
            codigoQR=tag.codigoQR,
            estado_tag=tag.estado,
            mensaje="¡Bienvenido a Encontrame! Esta chapita aún no está configurada. Regístrate o inicia sesión para asociarla a tu mascota.",
            mascota=None,
            veterinaria=tag.veterinaria,
        )

    # Caso 2: El tag ya está asignado a una mascota
    mascota = tag.mascota
    dueno = mascota.usuario

    # Registrar el evento de escaneo en la base de datos (auditoría / métrica de lectura)
    nuevo_escaneo = EscaneoTag(
        tag_id=tag.id,
        mascota_id=mascota.id,
        fecha_hora=datetime.now(timezone.utc),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(nuevo_escaneo)
    db.commit()

    # Construir información de contacto si el dueño la habilitó
    contacto_publico: Optional[ContactoDuenoPublic] = None
    if dueno and mascota.mostrar_telefono and dueno.telefono:
        mensaje_wa = f"¡Hola {dueno.nombre}! Acabo de escanear la chapita Encontrame de tu mascota {mascota.nombre}."
        wa_url = f"https://wa.me/{dueno.telefono.replace('+', '').replace(' ', '').replace('-', '')}?text={urllib.parse.quote(mensaje_wa)}"
        contacto_publico = ContactoDuenoPublic(
            nombre=dueno.nombre,
            telefono=dueno.telefono,
            telefono_secundario=dueno.telefono_secundario,
            whatsapp_url=wa_url,
        )

    perfil = PerfilMascotaScan(
        id=mascota.id,
        nombre=mascota.nombre,
        especie=mascota.especie,
        raza=mascota.raza,
        color=mascota.color,
        foto_url=mascota.foto_url,
        estado_extravio=mascota.estado_extravio,
        notas_medicas=mascota.notas_medicas,
        mensaje_personalizado=mascota.mensaje_personalizado,
        recompensa=mascota.recompensa,
        contacto=contacto_publico,
    )

    return TagScanResult(
        reclamado=True,
        token_publico=tag.token_publico,
        codigoQR=tag.codigoQR,
        estado_tag=tag.estado,
        mensaje="Mascota identificada con éxito",
        mascota=perfil,
        veterinaria=tag.veterinaria,
    )


@scan_routers.post("/{identificador}/reportar", status_code=status.HTTP_201_CREATED)
def reportar_avistamiento(
    identificador: str,
    datos: ReporteAvistamientoCreate,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Permite a quien encuentra a la mascota enviar su ubicación GPS y/o un mensaje de ayuda al dueño.
    No requiere instalar nada ni iniciar sesión.
    """
    tag = _buscar_tag_por_identificador(db, identificador)
    if not tag.mascota:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede reportar avistamiento para un tag sin mascota asignada",
        )

    escaneo = EscaneoTag(
        tag_id=tag.id,
        mascota_id=tag.mascota.id,
        fecha_hora=datetime.now(timezone.utc),
        latitud=datos.latitud,
        longitud=datos.longitud,
        mensaje_rescatista=datos.mensaje,
        telefono_rescatista=datos.telefono_contacto,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(escaneo)
    commit_or_409(db)
    db.refresh(escaneo)

    return {
        "status": "ok",
        "mensaje": "¡Gracias por ayudar! El aviso ha sido registrado para el dueño de la mascota.",
        "escaneo_id": escaneo.id,
    }


@scan_routers.post("/reclamar", response_model=MascotaPublic, status_code=status.HTTP_201_CREATED)
def reclamar_tag(
    datos: ReclamarTagRequest,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Permite al usuario autenticado (nuevo o existente) reclamar un tag virgen
    y configurar los datos de su mascota en una sola operación.
    """
    tag = _buscar_tag_por_identificador(db, datos.token_o_codigo)

    if tag.mascota is not None or tag.estado == EstadoTagEnum.RECLAMADO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este tag ya fue reclamado previamente y está vinculado a otra mascota",
        )

    # Crear la nueva mascota asignada al tag y al usuario autenticado
    nueva_mascota = Mascota(
        nombre=datos.nombre_mascota,
        especie=datos.especie,
        raza=datos.raza,
        color=datos.color,
        foto_url=datos.foto_url,
        notas_medicas=datos.notas_medicas,
        mensaje_personalizado=datos.mensaje_personalizado,
        mostrar_telefono=datos.mostrar_telefono,
        estado_extravio=EstadoMascotaEnum.EN_CASA,
        tag_id=tag.id,
        usuario_id=current_user.id,
    )
    db.add(nueva_mascota)

    # Actualizar estado del tag a RECLAMADO
    tag.estado = EstadoTagEnum.RECLAMADO
    tag.fecha_activacion = datetime.now(timezone.utc)
    db.add(tag)

    commit_or_409(db)
    db.refresh(nueva_mascota)
    return nueva_mascota

