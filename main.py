from fastapi import FastAPI
from db import create_tables
import estudiante
import curso

# Crear aplicación FastAPI
app = FastAPI(lifespan=create_tables, title="Sistema de Gestión Universitario")

# Incluir routers
app.include_router(estudiante.router, tags=["estudiante"], prefix="/estudiantes")
app.include_router(curso.router, tags=["curso"], prefix="/cursos")


