from pydantic import BaseModel, field_validator
from typing import Optional

class RolBase(BaseModel):
    id_rol: Optional[int] = None
    nombre: str

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, value: str):
        if not value or not value.strip():
            raise ValueError('El nombre del rol es obligatorio')
        return value.strip()

    class Config:
        from_attributes = True