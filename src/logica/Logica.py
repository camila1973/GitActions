from src.logica.Fachada_EPorra import Fachada_EPorra
from src.modelo.declarative_base import engine, Base, session
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class Logica(Fachada_EPorra):

    def __init__(self):
        Base.metadata.create_all(engine)
        # self.apostadores = [{'Nombre':'Pepe Pérez'},{'Nombre':"Ana Andrade"},{'Nombre':"Aymara Castillo"}]
        # self.apuestas = #[{'Apostador':'Pepe Pérez', 'Carrera':'Carrera 1', 'Valor':10, 'Competidor':'Juan Pablo Montoya'},\
        #                 {'Apostador':'Ana Andrade', 'Carrera':'Carrera 1', 'Valor':25, 'Competidor':'Michael Schumacher'},\
        #                 {'Apostador':'Aymara Castillo', 'Carrera':'Carrera 1', 'Valor':14, 'Competidor':'Juan Pablo Montoya'},\
        #                 {'Apostador':'Aymara Castillo', 'Carrera':'Carrera 2', 'Valor':45, 'Competidor':'Usain Bolt'}]
        # self.ganancias = [{'Carrera':'Formula 1', 'Ganancias':[('Pepe Pérez',13),('Ana Andrade',0), ('Aymara Castillo',15)], 'Ganancias de la casa': 4},\
        #     {'Carrera':'Atletismo 100 m planos', 'Ganancias':[('Pepe Pérez',32),('Ana Andrade',12), ('Aymara Castillo',34)], 'Ganancias de la casa': -10}]

    def dar_carreras(self): #Hace consulta a la bd y almacena en darcarreras la lista de las carreraras
        darcarrreras = [elem.__dict__ for elem in session.query(Carrera).all()] 
        return darcarrreras
    
    def dar_carrera(self, id_carrera): ##Hace consulta a la bd y almacena en darcarrera la lista de las carreraras y luego carrera en la posicion 
        darcarrera = [elem.__dict__ for elem in session.query(Carrera).all()]
        carrera = darcarrera[id_carrera]
        return carrera
        
        
    def crear_carrera(self, nombre):
        nueva_carrera = Carrera(Nombre = nombre, Abierta = True)
        session.add(nueva_carrera)
        session.commit()
        
    def editar_carrera(self, id, nombre):
        session.query(Carrera).filter(Carrera.id== id+1).update({"Nombre": nombre})
        session.commit()

    def validar_crear_editar_carrera(self, nombre, competidores):

        if len(nombre.strip()) == 0:
            return "El nombre carrera no puede estar vacío"

        # consulta = session.query(Carrera).filter(Carrera.Nombre == nombre).one_or_none()
        # if consulta:
        #     return "El nombre de la carrera ya existe"
        
        if len(competidores) == 0:
            return "no hay competidores"

        nombres_vistos = set()

        for competidor in competidores:
            nombre_competidor = competidor['Nombre'].strip()

            if not nombre_competidor:
                return "Hay competidores con nombres vacíos"
        
            if nombre_competidor in nombres_vistos:
                return "Hay competidores repetidos"
            else:
                nombres_vistos.add(nombre_competidor)  
            
        
            if competidor['Probabilidad'] is None:
                return "Hay competidores con probabilidades vacías"
            
            if not (0 <= competidor['Probabilidad'] <= 1):
                return "Hay probabilidades mayores a 1"
        
  
        suma_probabilidades = sum(competidor['Probabilidad'] for competidor in competidores)
        if suma_probabilidades > 1:
            return "La suma de las probabilidades no puede ser mayor a 1"
        
        if not suma_probabilidades==1:
            return "la suma de las probailidades no es igual a 1"

        return ""
        

    def terminar_carrera(self, id, ganador):
        session.query(Carrera).filter(Carrera.id== id+1).update({"Abierta": False})
        session.commit()
        session.query(Carrera).filter(Carrera.id== id+1).update({"ganador": ganador})
        session.commit()
        return None

    def eliminar_carrera(self, id):
        session.query(Carrera).filter(Carrera.id== id+1).delete()
        session.commit()
    
    def dar_apostadores(self):
        darapostadores = [elem.__dict__ for elem in session.query(Apostador).all()]
        return darapostadores

    def aniadir_apostador(self, nombre):
        nuevo_apostador=Apostador(Nombre=nombre)
        session.add(nuevo_apostador)
        session.commit()
        #print("session", session.new)
    
    # def editar_apostador(self, id, nombre):
    #     self.apostadores[id]['Nombre'] = nombre
    
    def validar_crear_editar_apostador(self, nombre):
        if len(nombre)!=0:
            consulta= session.query(Apostador).filter(Apostador.Nombre == nombre).one_or_none()
            if consulta:
                return f"El nombre ya existe"
            elif nombre.isdigit():
                return f"El nombre contiene numeros"
            else:
                return ""
        else :return "El nombre no puede estar vacío"

                
    
    # def eliminar_apostador(self, id):
    #     del self.apostadores[id]

    def dar_competidores_carrera(self, id):
        competidores= [elem.__dict__ for elem in session.query(Competidor).all()]
        competidores_carrera = [competidor for competidor in competidores if competidor['carrera_id'] == id+1] # se pone +1 porque la base de datos arranca en 1 y no en 0
        return competidores_carrera

    # def dar_competidor(self, id_carrera, id_competidor):
    #     return self.carreras[id_carrera]['Competidores'][id_competidor].copy()

    def aniadir_competidor(self, id, nombre, probabilidad):
        try:
            if not isinstance(probabilidad, float):
                raise ValueError("Hay competidores con probabilidades no válidas")
            else:
                carreras = [elem.__dict__ for elem in session.query(Carrera).all()] 
                id = len(carreras)
                nuevo_competidor = Competidor(Nombre = nombre, Probabilidad = probabilidad, carrera_id = id)
                session.add(nuevo_competidor)
                session.commit()
        except ValueError as e:
            print(e)
        
        
        #self.carreras[id]['Competidores'].append({'Nombre':nombre, 'Probabilidad':probabilidad})

    def editar_competidor(self, id_carrera, id_competidor, nombre, probabilidad):
        session.query(Competidor).filter(Competidor.id== id_competidor+1,Competidor.carrera_id== id_carrera+1).update({"Nombre": nombre})
        session.commit()
        session.query(Competidor).filter(Competidor.id== id_competidor+1,Competidor.carrera_id== id_carrera+1).update({"Probabilidad":probabilidad})
        session.commit()
        
    
    
    def eliminar_competidor(self, id_carrera, id_competidor):
        # session.query(Competidor).filter(Competidor.id== id_competidor).delete(synchronize_session=False)
        # session.commit()
        competidor=session.query(Competidor).filter(Competidor.id==id_competidor+1,Competidor.carrera_id== id_carrera+1).first()
        session.delete(competidor)
        session.commit()
        
        

    def dar_apuestas_carrera(self, id_carrera):

        resultados = session.query(
        Apostador.Nombre,
        Carrera.Nombre,
        Apuesta.Valor,
        Competidor.Nombre
    ).join(Apuesta, Apuesta.Apostador_id == Apostador.id) \
     .join(Carrera, Apuesta.Carrera_id == Carrera.id) \
     .join(Competidor, Apuesta.Competidor_id == Competidor.id) \
     .filter(Apuesta.Carrera_id == id_carrera+1) \
     .all()
        
        apuestas_lista = []
        for resultado in resultados:
            apuesta = {
                "Apostador": resultado[0],
                "Carrera": resultado[1],
                "Valor": resultado[2],
                "Competidor": resultado[3]
            }
            apuestas_lista.append(apuesta)

        return apuestas_lista

    # def dar_apuesta(self, id_carrera, id_apuesta):
    #     return self.dar_apuestas_carrera(id_carrera)[id_apuesta].copy()

    def crear_apuesta(self, apostador, id_carrera, valor, competidor):
        apostadorlist = session.query(Apostador).filter(Apostador.Nombre == apostador).all()
        apostadorlist = [elem.__dict__ for elem in apostadorlist]
        apostador1 = apostadorlist[0]["id"]
        competidorlist = session.query(Competidor).filter(Competidor.Nombre == competidor).all()
        competidorlist = [elem.__dict__ for elem in competidorlist]
        competidor1 = competidorlist[0]["id"]
        guardar_apuesta = Apuesta(Apostador_id=apostador1,Carrera_id=id_carrera+1,Valor=valor,Competidor_id=competidor1)
        session.add(guardar_apuesta)
        session.commit()

    #     n_apuesta = {}
    #     n_apuesta['Apostador'] = apostador
    #     n_apuesta['Carrera'] = self.carreras[id_carrera]['Nombre']
    #     n_apuesta['Valor'] = valor
    #     n_apuesta['Competidor'] = competidor
    #     self.apuestas.append(n_apuesta)

    # def editar_apuesta(self, id_apuesta, apostador, carrera, valor, competidor):
    #     self.apuestas[id_apuesta]['Apostador'] = apostador
    #     self.apuestas[id_apuesta]['Carrera'] = self.carreras[carrera]["Nombre"]
    #     self.apuestas[id_apuesta]['Valor'] = valor
    #     self.apuestas[id_apuesta]['Competidor'] = competidor

    def validar_crear_editar_apuesta(self, apostador,carrera, valor, competidor):
       
        if valor is None or len(str(valor).strip()) == 0:
            return "El campo Valor Apuesta no debe estar vacío"
        
        if not apostador or len(apostador.strip()) == 0:
            return "Debe seleccionar un apostador"
        
        if not competidor or len(competidor.strip()) == 0:
            return "Debe seleccionar un competidor"
        
        try:
            valor_float = float(valor)
        except ValueError:
            return "El campo Valor Apuesta debe ser un número válido"

        if len(str(int(valor_float))) > 10: 
            return "El campo Valor Apuesta debe tener una longitud máxima de 10 dígitos en la parte entera"
        
        if len(str(valor_float).split('.')[1]) > 5: 
            return "El campo Valor Apuesta debe tener una longitud máxima de 5 decimales"
        
     
        return ""



    # def eliminar_apuesta(self, id_carrera, id_apuesta):
    #     nombre_carrera =self.carreras[id_carrera]['Nombre']
    #     i = 0
    #     id = 0
    #     while i < len(self.apuestas):
    #         if self.apuestas[i]['Carrera'] == nombre_carrera:
    #             if id == id_apuesta:
    #                 self.apuestas.pop(i)
    #                 return True
    #             else:
    #                 id+=1
    #         i+=1
        
    #     return False
                

    #     del self.apuesta[id_apuesta]

    def dar_reporte_ganancias(self, id_carrera, id_competidor):
        # <-------descomentar cuando termine poner abajo
        resultados = session.query(
        Apostador.Nombre,
        Carrera.Nombre,
        Apuesta.Valor,
        Competidor.id,
        Competidor.Probabilidad
            ).join(Apuesta, Apuesta.Apostador_id == Apostador.id) \
            .join(Carrera, Apuesta.Carrera_id == Carrera.id) \
            .join(Competidor, Apuesta.Competidor_id == Competidor.id) \
            .filter(Apuesta.Carrera_id == id_carrera+1) \
            .all()
        
        competidores = session.query(Competidor.id).filter(Competidor.carrera_id == id_carrera+1).all()
        print('competidores', competidores, id_competidor)
        valores = [item[0] for item in competidores]        
        id_compnuevo = list(range(0, len(valores) + 1))
        id = valores[id_competidor]
        
        lganadores=[]
        sumabote = 0
        ganaciasapostadores = 0
        for r in resultados:
            apostador = r[0]
            apuesta = r[2]
            probabilidad = r[4]

            cuota = probabilidad / (1 - probabilidad)
            ganancia = apuesta + (apuesta/cuota)
            sumabote = sumabote + apuesta
            if r[3] == id:
                lganadores.append((apostador, round(ganancia,2)))
                ganaciasapostadores = ganaciasapostadores + round(ganancia,2)
            else:
                lganadores.append((apostador, 0))
        gananciacasa = round(sumabote,2) - round(ganaciasapostadores,2)
        self.terminar_carrera(id_carrera, id_competidor)
        return lganadores,gananciacasa
        # self.carreras[id_carrera]['Abierta']=False
        # n_carrera = self.carreras[id_carrera]['Nombre']
        # for ganancias in self.ganancias:
        #     if ganancias['Carrera'] == n_carrera:
        #         return ganancias['Ganancias'], ganancias['Ganancias de la casa']   