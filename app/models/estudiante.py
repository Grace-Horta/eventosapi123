from pydantic import BaseModel, field_validator
from typing import Optional

class EstudianteBase(BaseModel):
    id_estudiante: Optional[int] = None
    codigo: str
    id_usuario: int

    @field_validator('codigo')
    @classmethod
    def validar_codigo(cls, value: str):
        if not value or not value.strip():
            raise ValueError('El código de estudiante es obligatorio')
        return value.strip()

    class Config:
        from_attributes = True