from fastapi import APIRouter
from app.models.modelo_x_rol import ModeloXRolBase
from app.repositories.modelo_x_rol_repo import ModeloXRolRepository

router = APIRouter(prefix="/modelos-por-rol", tags=["Modelos Por Rol"])

@router.post("/")
def crear_modelo_x_rol(data: ModeloXRolBase):
    return {"id_modelo_por_rol": ModeloXRolRepository.crear(data)}