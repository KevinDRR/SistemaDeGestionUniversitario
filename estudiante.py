from typing import List, Optional
from fastapi import APIRouter, HTTPException
from models import Estudiante, EstudianteCreate, EstudianteUpdate, Matricula, Curso
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.get("/", response_model=List[Estudiante])
async def get_all_estudiantes(
    session: SessionDep, 
    semestre: Optional[int] = None,
    incluir_archivados: bool = False
):
    stmt = select(Estudiante)
    if semestre is not None:
        stmt = stmt.where(Estudiante.semestre == semestre)
    if not incluir_archivados:
        stmt = stmt.where(Estudiante.archivado == False)
    estudiantes = session.exec(stmt).all()
    return estudiantes

@router.delete("/{cedula}")
async def delete_estudiante(cedula: int, session: SessionDep):
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    estudiante.archivado = True  
    session.add(estudiante)
    session.commit()
    return {"message": "Estudiante archivado"}

@router.post("/", response_model=Estudiante)
async def create_estudiante(new_estudiante: EstudianteCreate, session: SessionDep):
    estudiante_data = new_estudiante.model_dump()
    estudiante = Estudiante.model_validate(estudiante_data)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.get("/{estudiante_id}")
async def get_one_estudiante(
    estudiante_id: int, 
    session: SessionDep,
    incluir_archivados: bool = False
):
    estudiante_db = session.get(Estudiante, estudiante_id)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    if estudiante_db.archivado and not incluir_archivados:
        raise HTTPException(status_code=404, detail="Estudiante archivado")
    stmt = select(Matricula).where(Matricula.estudiante_cedula == estudiante_id)
    matriculas = session.exec(stmt).all()
    cursos = []
    for m in matriculas:
        c = session.get(Curso, m.curso_id)
        if c:
            cursos.append(c)
    estudiante_dict = estudiante_db.model_dump()
    estudiante_dict["cursos"] = [c.model_dump() for c in cursos]
    return estudiante_dict

@router.put("/{estudiante_id}", response_model=Estudiante)
async def update_estudiante(estudiante_id: int, estudiante_update: EstudianteUpdate, session: SessionDep):
    estudiante_db = session.get(Estudiante, estudiante_id)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    update_data = estudiante_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(estudiante_db, key, value)

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)
    return estudiante_db