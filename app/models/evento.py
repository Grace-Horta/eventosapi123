from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha = Column(String, nullable=True)
    ubicacion = Column(String, nullable=True)
    categoria = Column(String, nullable=True)