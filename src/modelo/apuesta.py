from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
#from src.modelo.carrera import Carrera
from src.modelo.apostador import Apostador
from src.modelo.competidor import Competidor
from src.modelo.declarative_base import Base



class Apuesta(Base):
    
    __tablename__= 'apuesta'
    id = Column(Integer, primary_key=True)
    Apostador_id=Column(Integer,ForeignKey('apostador.id'))
    Carrera_id= Column(Integer,ForeignKey('carrera.id'))
    Valor= Column(Float)#este dato era floar, pero con este no se puede condicionar cantidad de digitos y decimales, entoces se cambia a numeric
    Competidor_id =Column(Integer,ForeignKey('competidor.id'))
    
    carrera = relationship('Carrera', back_populates='apuestas')
    apostador = relationship('Apostador', back_populates='apuestas')
    competidor = relationship('Competidor', back_populates='apuestas')
