from carrera import Carrera
from competidor import Competidor
from apuesta import Apuesta
from apostador import Apostador

from declarative_base import Session, engine, Base

if __name__ == '__main__':
    # Crear las tablas en la BD
    Base.metadata.create_all(engine)

    # Abrir una sesión
    session = Session()

    # Crear competidores
    competidor1 = Competidor(Nombre="Juan Pablo Montoya", Probabilidad=0.15)
    competidor2 = Competidor(Nombre="Kimi Räikkönen", Probabilidad=0.2)
    competidor3 = Competidor(Nombre="Michael Schumacher", Probabilidad=0.65)

    # Crear carrera
    carrera1 = Carrera(Nombre="Formula 1", Abierta=True)

    # Relacionar competidores con la carrera
    carrera1.competidores = [competidor1, competidor2, competidor3]

    # Añadir la carrera (esto también añadirá los competidores relacionados)
    session.add(carrera1)

    # Guardar cambios en la base de datos
    session.commit()

    competidor4 = Competidor(Nombre="Usain Bolt", Probabilidad=0.72)
    competidor5 = Competidor(Nombre="Lamont Marcell Jacobs", Probabilidad=0.13)
    competidor6 = Competidor(Nombre="Su Bingtian", Probabilidad=0.05)
    competidor7 = Competidor(Nombre="Robson da Silva", Probabilidad=0.1)

    carrera2 = Carrera(Nombre="Atletismo 100 m planos", Abierta=True)

    carrera2.competidores = [competidor4, competidor5, competidor6,competidor7]
    session.add(carrera2)
    session.commit()

    apostador1 = Apostador(Nombre="Pepe Pérez")
    apostador2 = Apostador(Nombre="Ana Andrade")
    apostador3 = Apostador(Nombre="Aymara Castillo")

    session.add_all([apostador1,apostador2,apostador3])
    session.commit()
    # apuesta1 = Apuesta(Apostador = apostador1,Carrera_id = 1,Valor = 10, Competidor= competidor1)
    # apuesta2 = Apuesta(Apostador = apostador2,Carrera_id = 1,Valor = 25, Competidor= competidor2)
    # apuesta3 = Apuesta(Apostador = apostador3,Carrera_id = 1,Valor = 14, Competidor= competidor1)
    # apuesta4 = Apuesta(Apostador = apostador3,Carrera_id = 2,Valor = 45, Competidor= competidor4)

    apuesta1 = Apuesta(Valor = 10, Apostador_id = apostador1.Nombre, Carrera_id = carrera1.Nombre, Competidor_id = competidor1.Nombre)
    apuesta2 = Apuesta(Valor = 25, Apostador_id = apostador2.Nombre, Carrera_id = carrera1.Nombre, Competidor_id = competidor2.Nombre)
    apuesta3 = Apuesta(Valor = 14, Apostador_id = apostador3.Nombre, Carrera_id = carrera1.Nombre, Competidor_id = competidor1.Nombre)
    apuesta4 = Apuesta(Valor = 45, Apostador_id = apostador3.Nombre, Carrera_id = carrera2.Nombre, Competidor_id = competidor4.Nombre)


    session.add_all([apuesta1,apuesta2,apuesta3,apuesta4])
    session.commit()

