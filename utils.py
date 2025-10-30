"""Funciones auxiliares para operaciones comunes de la base de datos."""

from typing import List
from sqlmodel import Session, select
from models import Matricula, Estudiante, Curso


def eliminar_matriculas_por_estudiante(session: Session, cedula: int) -> int:
    """
    Elimina todas las matrículas de un estudiante.
    
    Args:
        session: Sesión de base de datos
        cedula: Cédula del estudiante
    
    Returns:
        Número de matrículas eliminadas
    """
    stmt = select(Matricula).where(Matricula.estudiante_cedula == cedula)
    matriculas = session.exec(stmt).all()
    
    for matricula in matriculas:
        session.delete(matricula)
    
    return len(matriculas)


def eliminar_matriculas_por_curso(session: Session, curso_id: int) -> int:
    """
    Elimina todas las matrículas de un curso.
    
    Args:
        session: Sesión de base de datos
        curso_id: ID del curso
    
    Returns:
        Número de matrículas eliminadas
    """
    stmt = select(Matricula).where(Matricula.curso_id == curso_id)
    matriculas = session.exec(stmt).all()
    
    for matricula in matriculas:
        session.delete(matricula)
    
    return len(matriculas)


def obtener_cursos_de_estudiante(session: Session, cedula: int) -> List[Curso]:
    """
    Obtiene todos los cursos en los que está matriculado un estudiante.
    
    Args:
        session: Sesión de base de datos
        cedula: Cédula del estudiante
    
    Returns:
        Lista de cursos
    """
    # Query optimizado con JOIN
    stmt = (
        select(Curso)
        .join(Matricula, Curso.id == Matricula.curso_id)
        .where(Matricula.estudiante_cedula == cedula)
    )
    return list(session.exec(stmt).all())


def obtener_estudiantes_de_curso(session: Session, curso_id: int) -> List[Estudiante]:
    """
    Obtiene todos los estudiantes matriculados en un curso.
    
    Args:
        session: Sesión de base de datos
        curso_id: ID del curso
    
    Returns:
        Lista de estudiantes
    """
    # Query optimizado con JOIN
    stmt = (
        select(Estudiante)
        .join(Matricula, Estudiante.cedula == Matricula.estudiante_cedula)
        .where(Matricula.curso_id == curso_id)
    )
    return list(session.exec(stmt).all())
