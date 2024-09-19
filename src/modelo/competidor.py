from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
#from src.modelo.carrera import Carrera
from src.modelo.declarative_base import Base


class Competidor(Base):
    
    __tablename__= 'competidor'
    id = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Probabilidad = Column(Float)
    carrera_id= Column(Integer,ForeignKey('carrera.id'))
    carrera = relationship('Carrera', back_populates='competidores')
    apuestas= relationship('Apuesta', back_populates='competidor')