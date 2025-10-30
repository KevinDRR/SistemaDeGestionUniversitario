from fastapi import APIRouter, HTTPException
from models import Estudiante, EstudianteCreate
from db import SessionDep

router = APIRouter()

@router.post("/", response_model=Estudiante)
async def create_estudiante(new_estudiante: EstudianteCreate, session: SessionDep):
    estudiante_data = new_estudiante.model_dump()
    estudiante = Estudiante.model_validate(estudiante_data)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.get("/{estudiante_id}", response_model=Estudiante)
async def get_one_estudiante(estudiante_id: int, session: SessionDep):
    estudiante_db = session.get(Estudiante, estudiante_id)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante_db

@router.put("/{estudiante_id}", response_model=Estudiante)
async def update_estudiante(estudiante_id: int, estudiante_update: EstudianteCreate, session: SessionDep):
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