from typing import List, Optional
from fastapi import APIRouter, HTTPException
from models import Curso, CursoCreate, CursoUpdate, Estudiante, Matricula
from db import SessionDep
from sqlmodel import select
from utils import eliminar_matriculas_por_curso, obtener_estudiantes_de_curso, obtener_cursos_de_estudiante

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
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Eliminar matrículas asociadas usando función auxiliar
    matriculas_eliminadas = eliminar_matriculas_por_curso(session, curso_id)
    
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
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Obtener estudiantes usando función auxiliar optimizada
    estudiantes = obtener_estudiantes_de_curso(session, curso_id)
    
    # Construir respuesta con curso y sus estudiantes
    curso_dict = curso_db.model_dump()
    curso_dict["estudiantes"] = [e.model_dump() for e in estudiantes]
    return curso_dict

@router.put("/{curso_id}", response_model=Curso, status_code=200)
async def update_curso(curso_id: int, curso_update: CursoUpdate, session: SessionDep):
    """Actualiza los datos de un curso."""
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    update_data = curso_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")

    # Actualizar campos
    for key, value in update_data.items():
        setattr(curso_db, key, value)

    session.add(curso_db)
    session.commit()
    session.refresh(curso_db)
    return curso_db


@router.post("/{curso_id}/estudiantes/{cedula}", status_code=201)
async def matricular(curso_id: int, cedula: int, session: SessionDep):
    """Matricula un estudiante en un curso."""
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
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
    stmt = select(Matricula).where(
        Matricula.curso_id == curso_id,
        Matricula.estudiante_cedula == cedula,
    )
    existing = session.exec(stmt).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    
    session.delete(existing)
    session.commit()
    return {"message": "desmatriculado", "curso_id": curso_id, "cedula": cedula}


@router.get("/{curso_id}/estudiantes", status_code=200)
async def listar_estudiantes(curso_id: int, session: SessionDep):
    """Lista todos los estudiantes matriculados en un curso."""
    curso_db = session.get(Curso, curso_id)
    if not curso_db:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Obtener estudiantes usando función auxiliar optimizada
    return obtener_estudiantes_de_curso(session, curso_id)


@router.get("/estudiantes/{cedula}/cursos", status_code=200)
async def listar_cursos(cedula: int, session: SessionDep):
    """Lista todos los cursos en los que está matriculado un estudiante (incluye archivados)."""
    estudiante_db = session.get(Estudiante, cedula)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Obtener cursos usando función auxiliar optimizada
    # Nota: Permite ver cursos de estudiantes archivados
    return obtener_cursos_de_estudiante(session, cedula)