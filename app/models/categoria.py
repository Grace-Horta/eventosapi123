from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)