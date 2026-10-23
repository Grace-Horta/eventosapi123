from fastapi import APIRouter
from app.models.rol import RolBase
from app.repositories.rol_repo import RolRepository

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def crear_rol(data: RolBase):
    return {"id_rol": RolRepository.crear(data)}