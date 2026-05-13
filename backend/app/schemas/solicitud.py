from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class SolicitudCreate(BaseModel):
    cedula: str
    monto: float
    plazo_meses: int

    @field_validator("monto")
    @classmethod
    def validar_monto(cls, v):
        if v < 500 or v > 50000:
            raise ValueError("Monto debe estar entre $500 y $50,000")
        return v

    @field_validator("plazo_meses")
    @classmethod
    def validar_plazo(cls, v):
        if v < 6 or v > 60:
            raise ValueError("Plazo debe estar entre 6 y 60 meses")
        return v


class CambioEstado(BaseModel):
    estado: str
    comentario: str

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v):
        permitidos = {"pendiente", "aprobado", "rechazado"}
        if v not in permitidos:
            raise ValueError(f"Estado debe ser uno de: {permitidos}")
        return v


class SolicitudResponse(BaseModel):
    id: int
    cedula: str
    monto: float
    plazo_meses: int
    estado: str
    comentario: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
