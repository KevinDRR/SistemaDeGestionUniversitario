import datetime
from sqlmodel import SQLModel, Field

class CursoBase(SQLModel):
    """Modelo base para cursos con campos comunes."""
    id: int | None = Field(default=None, primary_key=True)
    nombre: str | None = Field(description="nombre del curso")
    Creditos: int | None = Field(description="creditos del curso")
    Horario: datetime.date | None = Field(description="horario del curso")

class EstudianteBase(SQLModel):
    """Modelo base para estudiantes con campos comunes."""
    cedula: int | None = Field(default=None, primary_key=True)
    nombre: str | None = Field(description="nombre del estudiante")
    email: str | None = Field(description="email del estudiante")
    semestre: int | None = Field(description="semestre del estudiante")


class Estudiante(EstudianteBase, table=True):
    """Modelo de tabla para estudiantes."""
    archivado: bool = Field(default=False, description="indica si el estudiante está archivado")

class Curso(CursoBase, table=True):
    """Modelo de tabla para cursos."""
    id: int | None = Field(default=None, primary_key=True)
 

class Matricula(SQLModel, table=True):
    """Modelo de tabla para matrículas (relación muchos-a-muchos)."""
    curso_id: int | None = Field(default=None, foreign_key="curso.id", primary_key=True)
    estudiante_cedula: int | None = Field(default=None, foreign_key="estudiante.cedula", primary_key=True)
    fecha: datetime.date | None = Field(default_factory=datetime.date.today)


class CursoCreate(CursoBase):
    """Esquema para crear un nuevo curso."""
    pass

class EstudianteCreate(EstudianteBase):
    """Esquema para crear un nuevo estudiante."""
    pass

class CursoUpdate(SQLModel):
    """Esquema para actualizar un curso (campos opcionales)."""
    nombre: str | None = None
    Creditos: int | None = None
    Horario: datetime.date | None = None

class EstudianteUpdate(SQLModel):
    """Esquema para actualizar un estudiante (campos opcionales)."""
    nombre: str | None = None
    email: str | None = None
    semestre: int | None = None

