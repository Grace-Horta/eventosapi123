from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=True)
    edificio = Column(String, nullable=True)