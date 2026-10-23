from fastapi import APIRouter
from app.models.estudiante import EstudianteBase
from app.repositories.estudiante_repo import EstudianteRepository

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.post("/")
def crear_estudiante(data: EstudianteBase):
    return {"id_estudiante": EstudianteRepository.crear(data)}