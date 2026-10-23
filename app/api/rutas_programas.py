from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.programa import Programa


class ProgramaSchema(BaseModel):
    nombre: str = Field(min_length=1)
    facultad_id: int


router = crear_crud("/programas", "Programas", Programa, ProgramaSchema)
