from typing import Optional
from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.categoria import Categoria


class CategoriaSchema(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: Optional[str] = None


router = crear_crud("/categorias", "Categorías", Categoria, CategoriaSchema)
