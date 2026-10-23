from pydantic import BaseModel, field_validator
from typing import Optional

class ModeloBase(BaseModel):
    id_modelo: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, value: str):
        if not value or not value.strip():
            raise ValueError('El nombre del modelo no puede estar vacío')
        return value.strip()

    class Config:
        from_attributes = True