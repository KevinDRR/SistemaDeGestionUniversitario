import datetime
from sqlmodel import SQLModel, Field

class CursoBase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str | None = Field(description= "nombre del curso")
    Creditos: int | None = Field(description= "creditos del curso")
    Horario: datetime.date | None = Field(description= "horario del curso")

class EstudianteBase(SQLModel, table=True):
    cedula: int | None = Field(default=None, primary_key=True)
    nombre: str | None = Field(description= "nombre del estudiante")
    email: str | None = Field(description= "email del estudiante")
    semestre: int | None = Field(description= "semestre del estudiante")


class Estudiante(EstudianteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class Curso(CursoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CursoCreate(CursoBase):
    pass

class EstudianteCreate(EstudianteBase):
    pass

class CursoUpdate(CursoBase):
    pass

class EstudianteUpdate(EstudianteBase):
    pass
