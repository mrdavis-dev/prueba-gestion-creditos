# Prueba — Gestión de Créditos

Sistema de gestión de solicitudes de crédito. Backend FastAPI + Frontend Angular, dockerizado.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI, SQLAlchemy, PyJWT, bcrypt |
| Frontend | Angular 19.2. |
| Base de datos | MySQL (AWS RDS) |
| Contenedores | Docker Compose |

## Requisitos

- Docker y Docker Compose instalados

## Levantar el proyecto

```bash
docker compose up --build
```

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:4200 |
| Backend API | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |

## Credenciales de acceso

| Campo | Valor |
|-------|-------|
| Usuario | `admin` |
| Contraseña | `admin123` |

## Variables de entorno

El backend requiere `backend/.env`:

```env
DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:3306/<db>
```
