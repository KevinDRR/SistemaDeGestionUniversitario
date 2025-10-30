from typing import List, Optional
from fastapi import APIRouter, HTTPException
from models import Curso, CursoCreate, CursoUpdate, Estudiante, EstudianteCreate, Matricula
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.get("/", response_model=List[Curso], status_code=200)
async def get_all_cursos(session: SessionDep, creditos: Optional[int] = None, codigo: Optional[int] = None):
    """Obtiene la lista de todos los cursos."""
    stmt = select(Curso)
    if creditos is not None:
        stmt = stmt.where(Curso.Creditos == creditos)
    if codigo is not None:
        stmt = stmt.where(Curso.id == codigo)
    cursos = session.exec(stmt).all()
    return cursos

@router.delete("/{curso_id}", status_code=200)
async def delete_curso(curso_id: int, session: SessionDep):
    """Elimina un curso y sus matrículas asociadas."""
    # Buscar curso
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Validar y eliminar matrículas asociadas
    stmt = select(Matricula).where(Matricula.curso_id == curso_id)
    matriculas = session.exec(stmt).all()
    
    matriculas_eliminadas = 0
    if len(matriculas) > 0:
        for matricula in matriculas:
            session.delete(matricula)
            matriculas_eliminadas += 1
    
    # Eliminar curso
    session.delete(curso)
    session.commit()
    
    return {
        "message": "Curso eliminado",
        "matriculas_eliminadas": matriculas_eliminadas
    }

@router.post("/", response_model=Curso, status_code=201)
async def create_curso(new_curso: CursoCreate, session: SessionDep):
    """Crea un nuevo curso."""
    # Convertir datos y crear curso
    curso_data = new_curso.model_dump()
    curso = Curso.model_validate(curso_data)
    
    # Guardar en base de datos
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

@router.get("/{curso_id}", status_code=200)
async def get_one_curso(curso_id: int, session: SessionDep):
    """Obtiene un curso con sus estudiantes matriculados."""
    # Buscar curso
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Obtener matrículas del curso
    stmt = select(Matricula).where(Matricula.curso_id == curso_id)
    matriculas = session.exec(stmt).all()
    
    # Obtener estudiantes de cada matrícula
    estudiantes = []
    for m in matriculas:
        est = session.get(Estudiante, m.estudiante_cedula)
        if est:
            estudiantes.append(est)
    
    # Construir respuesta con curso y sus estudiantes
    curso_dict = curso_db.model_dump()
    curso_dict["estudiantes"] = [e.model_dump() for e in estudiantes]
    return curso_dict

@router.put("/{curso_id}", response_model=Curso, status_code=200)
async def update_curso(curso_id: int, curso_update: CursoUpdate, session: SessionDep):
    """Actualiza los datos de un curso."""
    # Buscar curso
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    # Validar que se envió al menos un campo para actualizar
    update_data = curso_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    # Actualizar campos
    for key, value in update_data.items():
        setattr(curso_db, key, value)

    # Guardar cambios
    session.add(curso_db)
    session.commit()
    session.refresh(curso_db)
    return curso_db


@router.post("/{curso_id}/estudiantes/{cedula}", status_code=201)
async def matricular(curso_id: int, cedula: int, session: SessionDep):
    """Matricula un estudiante en un curso."""
    # Validar que existe el curso
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Validar que existe el estudiante
    estudiante_db = session.get(Estudiante, cedula)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Validar que no esté ya matriculado
    stmt = select(Matricula).where(
        Matricula.curso_id == curso_id,
        Matricula.estudiante_cedula == cedula,
    )
    existing = session.exec(stmt).first()
    if existing:
        raise HTTPException(status_code=409, detail="Estudiante ya matriculado en el curso")

    # Crear matrícula
    link = Matricula(curso_id=curso_id, estudiante_cedula=cedula)
    session.add(link)
    session.commit()
    return {"message": "matriculado", "curso_id": curso_id, "cedula": cedula}


@router.delete("/{curso_id}/estudiantes/{cedula}", status_code=200)
async def desmatricular(curso_id: int, cedula: int, session: SessionDep):
    """Desmatricula un estudiante de un curso."""
    # Buscar matrícula
    stmt = select(Matricula).where(
        Matricula.curso_id == curso_id,
        Matricula.estudiante_cedula == cedula,
    )
    existing = session.exec(stmt).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    
    # Eliminar matrícula
    session.delete(existing)
    session.commit()
    return {"message": "desmatriculado", "curso_id": curso_id, "cedula": cedula}


@router.get("/{curso_id}/estudiantes", status_code=200)
async def listar_estudiantes(curso_id: int, session: SessionDep):
    """Lista todos los estudiantes matriculados en un curso."""
    # Validar que existe el curso
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Obtener matrículas del curso
    stmt = select(Matricula).where(Matricula.curso_id == curso_id)
    matriculas = session.exec(stmt).all()
    
    # Obtener estudiantes
    estudiantes = []
    for m in matriculas:
        est = session.get(Estudiante, m.estudiante_cedula)
        if est:
            estudiantes.append(est)
    return estudiantes


@router.get("/estudiantes/{cedula}/cursos", status_code=200)
async def listar_cursos(cedula: int, session: SessionDep):
    """Lista todos los cursos en los que está matriculado un estudiante."""
    # Validar que existe el estudiante
    estudiante_db = session.get(Estudiante, cedula)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Obtener matrículas del estudiante
    stmt = select(Matricula).where(Matricula.estudiante_cedula == cedula)
    matriculas = session.exec(stmt).all()
    
    # Obtener cursos
    cursos = []
    for m in matriculas:
        c = session.get(Curso, m.curso_id)
        if c:
            cursos.append(c)
    return cursos