from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class SolicitudCredito(Base):
    __tablename__ = "solicitudes_credito"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String(20), nullable=False, index=True)
    monto = Column(Float, nullable=False)
    plazo_meses = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False, default="pendiente")
    comentario = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())