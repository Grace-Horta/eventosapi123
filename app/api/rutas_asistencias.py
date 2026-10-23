from typing import Optional
from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.asistencia import Asistencia


class AsistenciaSchema(BaseModel):
    evento_id: int
    asistente_email: str = Field(min_length=3)
    presente: Optional[bool] = False


# Solo Docentes y Administradores ven y registran asistencia.
router = crear_crud(
    "/asistencias", "Asistencias", Asistencia, AsistenciaSchema,
    roles_ver=("Administrador", "Docente"),
    roles_crear=("Administrador", "Docente"),
    roles_editar=("Administrador", "Docente"),
)
