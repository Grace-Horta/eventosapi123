from typing import Optional
from pydantic import BaseModel, Field
from app.api.crud import crear_crud
from app.models.organizador import Organizador


class OrganizadorSchema(BaseModel):
    nombre: str = Field(min_length=1)
    contacto: Optional[str] = None
    cargo: Optional[str] = None


router = crear_crud("/organizadores", "Organizadores", Organizador, OrganizadorSchema)
