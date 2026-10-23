from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base
from datetime import datetime

class Asistencia(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evento_id = Column(Integer, nullable=False)
    asistente_email = Column(String, nullable=False)
    presente = Column(Boolean, default=False)
    hora_registro = Column(DateTime, default=datetime.utcnow)