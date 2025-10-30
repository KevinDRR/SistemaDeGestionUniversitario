# Sistema de Gestión Universitario 

API REST para la gestión de estudiantes, cursos y matrículas universitarias desarrollada con FastAPI y SQLModel.

## Descripción

Sistema completo de gestión universitaria que permite:
- Gestionar estudiantes (CRUD completo)
- Gestionar cursos (CRUD completo)
- Matricular y desmatricular estudiantes en cursos
- Consultas relacionales (estudiantes con sus cursos y viceversa)
- Archivar estudiantes manteniendo integridad referencial

## Características

- API RESTful con FastAPI
- Base de datos SQLite con SQLModel
- Validaciones de integridad referencial
- Códigos de estado HTTP apropiados (200, 201, 400, 404, 409)
- Documentación
- Relaciones muchos-a-muchos (Estudiante ↔ Curso)
- Soft delete (archivado de estudiantes)

## Estructura del Proyecto

```
SistemaDeGestionUniversitario/
├── main.py              # Punto de entrada de la aplicación
├── db.py                # Configuración de base de datos
├── models.py            # Modelos de datos (SQLModel)
├── estudiante.py        # Router de endpoints de estudiantes
├── curso.py             # Router de endpoints de cursos
├── requirements.txt     # Dependencias del proyecto
├── test_main.http       # Pruebas HTTP
└── Universidad.sqlite3  # Base de datos SQLite
```

## Tecnologías

- **Python 3.10+**
- **FastAPI 0.104.1** - Framework web moderno
- **SQLModel 0.0.11** - ORM basado en Pydantic y SQLAlchemy
- **Uvicorn 0.24.0** - Servidor ASGI

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/KevinDRR/SistemaDeGestionUniversitario.git
cd SistemaDeGestionUniversitario
```

### 2. Crear entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

### Iniciar el servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`

### Acceder a la documentación

- http://127.0.0.1:8000/docs

## API Endpoints

### Estudiantes

| Método | Endpoint | Descripción | Código |
|--------|----------|-------------|--------|
| `GET` | `/estudiantes` | Lista todos los estudiantes | 200 |
| `GET` | `/estudiantes/{id}` | Obtiene un estudiante con sus cursos | 200, 404 |
| `POST` | `/estudiantes` | Crea un nuevo estudiante | 201, 409 |
| `PUT` | `/estudiantes/{id}` | Actualiza un estudiante | 200, 400, 404 |
| `DELETE` | `/estudiantes/{id}` | Archiva un estudiante | 200, 400, 404 |

### Cursos

| Método | Endpoint | Descripción | Código |
|--------|----------|-------------|--------|
| `GET` | `/cursos` | Lista todos los cursos | 200 |
| `GET` | `/cursos/{id}` | Obtiene un curso con sus estudiantes | 200, 404 |
| `POST` | `/cursos` | Crea un nuevo curso | 201 |
| `PUT` | `/cursos/{id}` | Actualiza un curso | 200, 400, 404 |
| `DELETE` | `/cursos/{id}` | Elimina un curso | 200, 404 |

### Matrículas

| Método | Endpoint | Descripción | Código |
|--------|----------|-------------|--------|
| `POST` | `/cursos/{id}/estudiantes/{cedula}` | Matricula un estudiante | 201, 404, 409 |
| `DELETE` | `/cursos/{id}/estudiantes/{cedula}` | Desmatricula un estudiante | 200, 404 |
| `GET` | `/cursos/{id}/estudiantes` | Lista estudiantes de un curso | 200, 404 |
| `GET` | `/cursos/estudiantes/{cedula}/cursos` | Lista cursos de un estudiante | 200, 404 |

## Ejemplos de Uso

### Crear un estudiante

```http
POST http://127.0.0.1:8000/estudiantes
Content-Type: application/json

{
    "cedula": 1,
    "nombre": "Kevin Rodríguez",
    "email": "kevin@universidad.edu",
    "semestre": 6
}
```

### Crear un curso

```http
POST http://127.0.0.1:8000/cursos
Content-Type: application/json

{
    "nombre": "Desarrollo de Software",
    "Creditos": 4,
    "Horario": "2025-10-30"
}
```

### Matricular estudiante en curso

```http
POST http://127.0.0.1:8000/cursos/1/estudiantes/1
```

### Obtener estudiante con sus cursos

```http
GET http://127.0.0.1:8000/estudiantes/1
```

**Respuesta:**
```json
{
    "cedula": 1,
    "nombre": "Kevin Rodríguez",
    "email": "kevin@universidad.edu",
    "semestre": 6,
    "archivado": false,
    "cursos": [
        {
            "id": 1,
            "nombre": "Desarrollo de Software",
            "Creditos": 4,
            "Horario": "2025-10-30"
        }
    ]
}
```

## Modelos de Datos

### Estudiante
- `cedula` (int, PK): Cédula del estudiante
- `nombre` (str): Nombre completo
- `email` (str): Correo electrónico
- `semestre` (int): Semestre actual
- `archivado` (bool): Estado de archivado

### Curso
- `id` (int, PK): ID del curso
- `nombre` (str): Nombre del curso
- `Creditos` (int): Cantidad de créditos
- `Horario` (date): Fecha del horario

### Matrícula
- `curso_id` (int, FK, PK): ID del curso
- `estudiante_cedula` (int, FK, PK): Cédula del estudiante
- `fecha` (date): Fecha de matrícula

## Características Técnicas

### Validaciones Implementadas
- Prevención de duplicados (409 Conflict)
- Validación de existencia de recursos (404 Not Found)
- Validación de datos requeridos (400 Bad Request)
- Integridad referencial en eliminaciones

### Soft Delete
Cuando se elimina un estudiante:
1. Se marca como `archivado = True`
2. Se eliminan todas sus matrículas
3. Se retorna el número de matrículas eliminadas

### Consultas Relacionales
- `GET /estudiantes/{id}` → Retorna estudiante con sus cursos
- `GET /cursos/{id}` → Retorna curso con sus estudiantes

## Pruebas

El archivo `test_main.http` contiene ejemplos de todas las operaciones disponibles. Puedes usarlo con la extensión REST Client de VS Code.

## Códigos de Estado HTTP

| Código | Significado | Uso                                   |
|--------|-------------|---------------------------------------|
| 200    | OK          | Operación exitosa (GET, PUT, DELETE)  |
| 201    | Created     | Recurso creado exitosamente (POST)    |
| 400    | Bad Request | Datos inválidos o faltantes           |
| 404    | Not Found   | Recurso no encontrado                 |
| 409    | Conflict    | Conflicto (duplicado, ya matriculado) |

