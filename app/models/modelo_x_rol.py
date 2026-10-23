from pydantic import BaseModel, field_validator
from typing import Optional

class ModeloXRolBase(BaseModel):
    id_modelo_por_rol: Optional[int] = None
    id_rol: int
    id_modelo: int
    puede_crear: bool = False
    puede_leer: bool = True
    puede_actualizar: bool = False
    puede_eliminar: bool = False

    @field_validator('id_rol', 'id_modelo')
    @classmethod
    def validar_ids(cls, value: int):
        if value <= 0:
            raise ValueError('Los IDs de rol y modelo deben ser enteros positivos')
        return value

    class Config:
        from_attributes = True