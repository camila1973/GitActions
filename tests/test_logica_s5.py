import unittest
from faker import Faker
from src.modelo.competidor import Competidor
from src.modelo.carrera import Carrera
from src.logica.Logica import Logica
from src.modelo.declarative_base import Session
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

		#print(self.data[i],"Nombre")

		self.session.commit()

	
	# def setUp(self):
	# 	self.session = Session()
	# 	self.logica = Logica()
	def tearDown(self) -> None:
		self.session.query(Competidor).delete()
		self.session.query(Carrera).delete()
		self.session.commit()
		self.session.close
	
	def test_editar_competidor(self):
		self.logica.editar_competidor(0,0,"Juan",0.9)
		consulta= self.session.query(Competidor).filter(Competidor.id== 1).first()
		self.assertEqual(consulta.Nombre, "Juan")

	# def test_eliminar_competidor(self):
	# 	id_carrera = 1
	# 	id_competidor = 1
	# 	self.logica.eliminar_competidor(id_carrera, id_competidor)
	# 	for competidor in self.logica.competidor:
	# 		if competidor['id'] == id_competidor:
	# 			test = False
	# 		else: 
	# 			test = True
	# 	self.assertFalse(test)


	def test_editar_carrera(self): # este es funcional
		self.logica.editar_carrera(0,'Formula 3')
		consulta= self.session.query(Carrera).filter(Carrera.id== 1).first()
		self.assertEqual(consulta.Nombre, "Formula 3")
		
	
	def test_eliminar_carrera(self):#este es funcional
		id_carrera = 0
		self.logica.eliminar_carrera(id_carrera)
		consulta= self.session.query(Carrera).filter(Carrera.id== id_carrera+1).all()
		consulta= [elem.__dict__ for elem in consulta] 
		self.assertEqual(consulta, [])