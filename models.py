import datetime
from sqlmodel import SQLModel, Field

class CursoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str | None = Field(description= "nombre del curso")
    Creditos: int | None = Field(description= "creditos del curso")
    Horario: datetime.date | None = Field(description= "horario del curso")

class EstudianteBase(SQLModel):
    cedula: int | None = Field(default=None, primary_key=True)
    nombre: str | None = Field(description= "nombre del estudiante")
    email: str | None = Field(description= "email del estudiante")
    semestre: int | None = Field(description= "semestre del estudiante")


class Estudiante(EstudianteBase, table=True):
    cedula: int | None = Field(default=None, primary_key=True)

class Curso(CursoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
 

class Matricula(SQLModel, table=True):
    curso_id: int | None = Field(default=None, foreign_key="curso.id", primary_key=True)
    estudiante_cedula: int | None = Field(default=None, foreign_key="estudiante.cedula", primary_key=True)
    fecha: datetime.date | None = Field(default_factory=datetime.date.today)


class CursoCreate(CursoBase):
    pass

class EstudianteCreate(EstudianteBase):
    pass

class CursoUpdate(SQLModel):
    nombre: str | None = None
    Creditos: int | None = None
    Horario: datetime.date | None = None

class EstudianteUpdate(SQLModel):
    nombre: str | None = None
    email: str | None = None
    semestre: int | None = None

