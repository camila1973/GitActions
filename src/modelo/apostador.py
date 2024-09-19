from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.modelo.declarative_base import Base



class Apostador(Base):
    
    __tablename__= 'apostador'
    id = Column(Integer, primary_key=True)
    Nombre = Column(String)
    apuestas = relationship('Apuesta', back_populates='apostador')