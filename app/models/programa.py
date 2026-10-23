from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Programa(Base):
    __tablename__ = "programas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    facultad_id = Column(Integer, nullable=False)