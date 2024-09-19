import unittest
from faker import Faker
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.carrera import Carrera
from src.logica.Logica import Logica
from src.modelo.declarative_base import Session
from sqlalchemy import desc,func
import random



class ExampleTestCase(unittest.TestCase):

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
		self.apostadores=[]
		self.apuestas=[]
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

		for u in range(5):
			nuevo_apostador=Apostador(Nombre= self.data_factory.unique.name())
			self.apostadores.append(nuevo_apostador)
			self.session.add(nuevo_apostador)
			self.session.commit()
			#print(self.apostadores[-1])
		self.consulta=self.session.query(Apostador).all
		#print(self.consulta)

		
		for carrera in  self.carreras:
			for competidor in self.competidores:
				apostador_asignado=random.choice(self.apostadores)
				nueva_apuesta=Apuesta(
					Valor=self.data_factory.pyfloat(min_value=1, max_value=100, right_digits=2),
					Competidor_id=competidor.id,
					Carrera_id=carrera.id,
					Apostador_id=apostador_asignado.id
				)
				self.apuestas.append(nueva_apuesta)
				self.session.add(nueva_apuesta)

		#print(self.data[i],"Nombre")

		self.session.commit()

	
	# def setUp(self):
	# 	self.session = Session()
	# 	self.logica = Logica()
	def tearDown(self) -> None:
		self.session.query(Competidor).delete()
		self.session.query(Carrera).delete()
		self.session.query(Apostador).delete()
		self.session.query(Apuesta).delete()
		self.session.commit()
		self.session.close

	def test_dar_apuestas_carrera(self):
		"HU011 se valida que liste dar apuestas con las 21 cargadas en el setUp"
		lista=self.logica.dar_apuestas_carrera(1)
		self.assertEqual(len(lista),21)





	