from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.modelo.apuesta import Apuesta
from src.modelo.declarative_base import Base

#Relacion uno a muchos con competidor

class Carrera(Base):
    __tablename__= 'carrera'
    id = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Abierta = Column(Boolean)
    ganador = Column(String, nullable=True, default=None)
    competidores = relationship('Competidor', back_populates='carrera')
    apuestas= relationship('Apuesta', back_populates='carrera')