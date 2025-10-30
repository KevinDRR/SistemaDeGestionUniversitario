from fastapi import FastAPI
from db import create_tables
import estudiante
import curso

app = FastAPI(lifespan=create_tables, title="Cursos API")
app = FastAPI(lifespan=create_tables, title="Estudiantes API")
app.include_router(estudiante.router, tags=["estudiante"], prefix="/estudiantes")
app.include_router(curso.router, tags=["curso"], prefix="/cursos")


