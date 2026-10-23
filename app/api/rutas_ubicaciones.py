from typing import Optional
from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.ubicacion import Ubicacion


class UbicacionSchema(BaseModel):
    nombre: str = Field(min_length=1)
    capacidad: Optional[int] = None
    edificio: Optional[str] = None


router = crear_crud("/ubicaciones", "Ubicaciones", Ubicacion, UbicacionSchema)
