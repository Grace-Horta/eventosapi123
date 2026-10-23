from fastapi import APIRouter
from app.models.modelo import ModeloBase
from app.repositories.modelo_repo import ModeloRepository

router = APIRouter(prefix="/modelos", tags=["Modelos"])

@router.post("/")
def crear_modelo(data: ModeloBase):
    return {"id_modelo": ModeloRepository.crear(data)}