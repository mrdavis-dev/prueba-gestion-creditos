from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import SolicitudCredito  # noqa: F401
from app.routers import solicitudes_router, auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestión de Créditos API") #docs_url=None, redoc_url=None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(solicitudes_router)
