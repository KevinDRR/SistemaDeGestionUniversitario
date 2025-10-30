from fastapi import APIRouter, HTTPException
from models import Curso, CursoCreate, Estudiante, EstudianteCreate
from db import SessionDep

router = APIRouter()

@router.post("/", response_model=Curso)
async def create_curso(new_curso: CursoCreate, session: SessionDep):
    curso_data = new_curso.model_dump()
    curso = Curso.model_validate(curso_data)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

@router.get("/{curso_id}", response_model=Curso)
async def get_one_curso(curso_id: int, session: SessionDep):
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso_db

@router.put("/{curso_id}", response_model=Curso)
async def update_curso(curso_id: int, curso_update: CursoCreate, session: SessionDep):
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    update_data = curso_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(curso_db, key, value)

    session.add(curso_db)
    session.commit()
    session.refresh(curso_db)
    return curso_db