from typing import Optional
from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.facultad import Facultad


class FacultadSchema(BaseModel):
    nombre: str = Field(min_length=1)
    decano: Optional[str] = None


router = crear_crud("/facultades", "Facultades", Facultad, FacultadSchema)
