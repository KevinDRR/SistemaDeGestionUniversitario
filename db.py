from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated

# Configuración de la base de datos
db_name = "Universidad.sqlite3"
db_url = f"sqlite:///{db_name}"

# Motor de base de datos
engine = create_engine(db_url)

def create_tables(app:FastAPI):
    """Crea todas las tablas en la base de datos al iniciar la aplicación."""
    SQLModel.metadata.create_all(engine)
    yield

def get_session() -> Session:
    """Proporciona una sesión de base de datos para cada request."""
    with Session(engine) as session:
        yield session

# Dependencia de sesión para FastAPI
SessionDep = Annotated[Session, Depends(get_session)]
