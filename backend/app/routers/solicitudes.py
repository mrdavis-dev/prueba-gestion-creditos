from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.solicitud import SolicitudCredito
from app.models.user import User
from app.schemas.solicitud import SolicitudCreate, CambioEstado, SolicitudResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/solicitudes", tags=["solicitudes"])


@router.post("/", response_model=SolicitudResponse, status_code=201)
def crear_solicitud(
    solicitud: SolicitudCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    nueva = SolicitudCredito(**solicitud.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.get("/", response_model=List[SolicitudResponse])
def listar_solicitudes(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(SolicitudCredito)
    if estado:
        query = query.filter(SolicitudCredito.estado == estado)
    return query.order_by(SolicitudCredito.created_at.desc()).all()


@router.patch("/{solicitud_id}/estado", response_model=SolicitudResponse)
def cambiar_estado(
    solicitud_id: int,
    cambio: CambioEstado,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    solicitud = db.query(SolicitudCredito).filter(SolicitudCredito.id == solicitud_id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    if solicitud.estado != "pendiente":
        raise HTTPException(
            status_code=400,
            detail=f"Solicitud ya fue {solicitud.estado}, no se puede modificar",
        )
    solicitud.estado = cambio.estado
    solicitud.comentario = cambio.comentario
    db.commit()
    db.refresh(solicitud)
    return solicitud
