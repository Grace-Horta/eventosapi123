from pydantic import BaseModel, field_validator
from typing import Optional

class CertificadoBase(BaseModel):
    id_certificado: Optional[int] = None
    codigo_validacion: str
    id_asistencia: int

    @field_validator('codigo_validacion')
    @classmethod
    def validar_codigo(cls, value: str):
        if not value or not value.strip():
            raise ValueError('El código de validación es obligatorio')
        return value.strip()

    class Config:
        from_attributes = True