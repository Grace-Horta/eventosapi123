from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Facultad(Base):
    __tablename__ = "facultades"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)
    decano = Column(String, nullable=True)