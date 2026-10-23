from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="Estudiante")  # Administrador | Docente | Estudiante
    activo = Column(Boolean, nullable=False, default=True)
