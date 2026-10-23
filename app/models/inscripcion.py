from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evento_id = Column(Integer, nullable=False)
    usuario_nombre = Column(String, nullable=False)
    usuario_email = Column(String, nullable=False)
    estado = Column(String, default="Pendiente")
    fecha_inscripcion = Column(DateTime, default=datetime.utcnow)