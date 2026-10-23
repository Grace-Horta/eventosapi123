from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Organizador(Base):
    __tablename__ = "organizadores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    contacto = Column(String, nullable=True)
    cargo = Column(String, nullable=True)