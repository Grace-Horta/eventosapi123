from typing import Optional
from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.evento import Evento


class EventoSchema(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: Optional[str] = None
    fecha: Optional[str] = None
    ubicacion: Optional[str] = None
    categoria: Optional[str] = None


router = crear_crud("/eventos", "Eventos", Evento, EventoSchema)
