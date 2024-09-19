import unittest
from faker import Faker
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.logica.Logica import Logica
from src.modelo.declarative_base import Session
import random

class funcTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.logica = Logica()
        self.data_factory = Faker()
        Faker.seed(1000)
        if hasattr(self, 'skip_setUp') and self.skip_setUp:
            return 
        
        self.data=[]
        self.carreras=[]
        self.competidores=[]
        self.races=["atletismo1","caballos","MotoGP","Formula 1", "100M Planos","Premio Monaco", "Natacion"]
        self.data=random.sample(self.races,7)# se utiliza para que los nombres de las carreras no se repitan
  
        for i in range(0,7):
  
            nueva_carrera=Carrera(Nombre=self.data[i],Abierta=True)
            self.carreras.append(nueva_carrera)
            self.session.add(self.carreras[-1])
            self.session.commit() 

            for j in range(3):
                self.nuevo_competidor=Competidor(
                    Nombre=self.data_factory.unique.name(),
                    Probabilidad=self.data_factory.pyfloat(min_value=0, max_value=1,right_digits=4),
                    carrera_id=nueva_carrera.id
                )
                self.competidores.append(self.nuevo_competidor)
                self.session.add(self.nuevo_competidor)
                self.session.commit()
    

        
        self.session.commit()

    def tearDown(self) -> None:
        self.session.query(Competidor).delete()
        self.session.query(Carrera).delete()
        self.session.commit()
        self.session.close

    def test_dar_carreras_vacio(self): # esta prueba solo corre con la bd vacia y sin otros test.
        self.skip_setUp=True
        self.session.query(Competidor).delete()
        self.session.query(Carrera).delete()
        self.session.commit()
        self.session.close
        consulta = self.logica.dar_carreras()
        self.assertEqual(len(consulta), 0)
    
    def test_dar_carreras(self):
        consulta1 = self.logica.dar_carreras()
        self.logica.crear_carrera("Natacion")
        consulta2 = self.logica.dar_carreras()
        self.assertGreaterEqual(len(consulta2), len(consulta1))

    def test_crear_carrera(self):
        self.logica.crear_carrera("Ciclismo")
        self.logica.crear_carrera("MotoGP")
        consulta1 = self.session.query(Carrera).filter(Carrera.Nombre == "Ciclismo").first()
        consulta2 = self.session.query(Carrera).filter(Carrera.id == 2).first()
        self.assertIsNotNone(consulta2)
        self.assertEqual(consulta1.Nombre, "Ciclismo")

    def test_dar_carrera(self): #Se debe correr con la bd con datos precargados
        consulta1 = self.logica.dar_carrera(1)
        self.logica.crear_carrera("Natacion2")
        consulta2 = self.logica.dar_carrera(1)
        self.assertGreaterEqual(len(consulta2), len(consulta1))

    def test_dar_competidores_carrera_vacio(self): #Se debe probar con una carrera sin competidores en la bd
        self.session.query(Competidor).delete()
        self.session.query(Carrera).delete()
        self.session.commit()
        self.session.close
        consulta = self.logica.dar_competidores_carrera(3)
        self.assertEqual(len(consulta), 0)

    def test_dar_competidores_carera(self):
        consulta1 = self.logica.dar_competidores_carrera(1)
        self.logica.aniadir_competidor(-1,"Camila",0.6)
        consulta2 = self.logica.dar_competidores_carrera(1)
        #print(consulta2)
        self.assertIsNotNone(consulta2)
        self.assertGreaterEqual(len(consulta2), len(consulta1))

    def test_aniadir_competidor(self):# Se debe porbar con la bd con los datos precargados
        self.logica.aniadir_competidor(-1,"Camila",0.6)
        consulta2 = self.logica.dar_competidores_carrera(3)
        #print(consulta2)
        self.assertIsNotNone(consulta2)