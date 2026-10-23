from typing import Optional
from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.inscripcion import Inscripcion


class InscripcionSchema(BaseModel):
    evento_id: int
    usuario_nombre: str = Field(min_length=1)
    usuario_email: str = Field(min_length=3)
    estado: Optional[str] = "Pendiente"


# Cualquier usuario con sesión puede inscribirse; solo el Administrador edita o elimina.
router = crear_crud(
    "/inscripciones", "Inscripciones", Inscripcion, InscripcionSchema,
    roles_ver=(), roles_crear=(), roles_editar=("Administrador",),
)
