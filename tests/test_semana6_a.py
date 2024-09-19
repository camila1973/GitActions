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

def validar_float(valor):
	
    valor_str = f"{valor:.5f}"
    parte_entera, parte_decimal = valor_str.split(".")
    
    if len(parte_entera) > 10 or len(parte_decimal) > 5:
        return False
    return True

def validar_ganancias_no_none(ganancias):
    for _, ganancia in ganancias:
        if ganancia is None:
            return False
    return True

def validar_nombres_no_vacios(ganancias):
    for nombre, _ in ganancias:# el _ ignora el valor de la tupla en este caso la ganancia
        if not nombre:
            return False
    return True

def validar_ganancias_casa_no_none(ganancias):
    #for _, ganancia in ganancias:
	if ganancias is None:
		return False
	return True

def crear_modelo_ganancias(self):
		nombre = "Formula1"
		nueva_carrera = Carrera(Nombre = nombre, Abierta = True)
		self.session.add(nueva_carrera)
		self.session.commit()
		carreras = [elem.__dict__ for elem in self.session.query(Carrera).all()] 
		id = len(carreras)
		#se crean competidores
		nombre = "Fran"
		probabilidad = 0.4
		nuevo_competidor = Competidor(Nombre = nombre, Probabilidad = probabilidad, carrera_id = id)
		self.session.add(nuevo_competidor)
		self.session.commit()
		nombre = "Tomas"
		probabilidad = 0.6
		nuevo_competidor = Competidor(Nombre = nombre, Probabilidad = probabilidad, carrera_id = id)
		self.session.add(nuevo_competidor)
		self.session.commit()
		nombre = "Pedro"
		probabilidad = 0.6
		nuevo_competidor = Competidor(Nombre = nombre, Probabilidad = probabilidad, carrera_id = id)
		self.session.add(nuevo_competidor)
		self.session.commit()
		#se crean apostadores
		nombre = "Pedro Perez"
		nuevo_apostador=Apostador(Nombre= nombre)
		self.apostadores.append(nuevo_apostador)
		self.session.add(nuevo_apostador)
		self.session.commit()
		nombre = "Camila G"
		#Se crean apuestas
		nuevo_apostador=Apostador(Nombre= nombre)
		self.apostadores.append(nuevo_apostador)
		self.session.add(nuevo_apostador)
		self.session.commit()
		nueva_apuesta1=Apuesta(Apostador_id=1,Carrera_id=1,Valor=100,Competidor_id=1)
		self.apuestas.append(nueva_apuesta1)
		self.session.add(nueva_apuesta1)
		self.session.commit()
		nueva_apuesta2=Apuesta(Apostador_id=2,Carrera_id=1,Valor=10,Competidor_id=2)
		self.apuestas.append(nueva_apuesta2)
		self.session.add(nueva_apuesta2)
		self.session.commit()

def consulta_aleatoria(self):
		idCar=random.randint(0,len(self.carreras)-1)
		l_competidor_id = []
		for competidor in self.competidores:
			if competidor.carrera_id == idCar+1:
				l_competidor_id.append(competidor.id)
		idCom = random.choice(l_competidor_id)
		idApos = random.randint(0,len(self.apostadores)-1)
		
		return idCar,idCom,idApos

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
			
		self.consulta=self.session.query(Apostador).all
		
		
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

		

		self.session.commit()
		
	def tearDown(self) -> None:
		self.session.query(Competidor).delete()
		self.session.query(Carrera).delete()
		self.session.query(Apostador).delete()
		self.session.query(Apuesta).delete()
		self.session.commit()
		self.session.close



	def test_validar_crear_editar_carrera_vacio(self):
		"HU001 validar que nombre de carrera no este vacio"
		validacion=self.logica.validar_crear_editar_carrera("","")
		self.assertEqual(validacion, "El nombre carrera no puede estar vacío")

	def test_validar_crear_editar_carrera_duplicada(self):
		"HU001 validar que nombre de carrera no este duplicado"
		carreras= [elem.__dict__ for elem in self.session.query(Carrera).all()]
		carrera_random=random.choice(carreras)
		carrera_id=carrera_random["id"]
		competidores =[elem.__dict__ for elem in self.session.query(Competidor).filter(Competidor.carrera_id == carrera_id).all()]

	def test_dar_apostador(self):
		"HU005 Se prueba que este enviando los 5 apostadores creados en setUP"
		lista=self.logica.dar_apostadores()
		self.assertEqual(len(lista),5)

	#@unittest.skip("Trabajo en progreso, será habilitado nuevamente")
	def test_dar_apostador_vacio(self):
		"HU005 Se prueba que devuelva lista vacia de apostadores"
		self.session.query(Apostador).delete()
		self.session.commit()
		self.session.close
		lista=self.logica.dar_apostadores()
		self.assertEqual(len(lista),0)


	def test_aniadir_apostador_exitoso(self):
		"HU006 Se prueba que se añada nuevo apostador"
		total_apostadores=self.session.query(Apostador).count()
		nombre_aleatario=self.data_factory.unique.name()
		self.logica.aniadir_apostador(nombre_aleatario)
		# self.session.commit()
		id_nuevo_apostador=self.session.query(Apostador).count()
		self.assertGreaterEqual(id_nuevo_apostador,total_apostadores)
		self.logica.aniadir_apostador(nombre_aleatario)
		consulta1 = self.session.query(Apostador).filter(Apostador.Nombre == nombre_aleatario).first()
		self.assertEqual(consulta1.Nombre, nombre_aleatario)

	def test_validar_crear_editar_apostador_vacio(self):
		"HU006 se valida que el nombre no este vacío"
		validacion=self.logica.validar_crear_editar_apostador('')
		self.assertEqual(validacion, "El nombre no puede estar vacío")


	def test_validar_crear_editar_apostador_duplicado(self):
		"HU006 se valida que el nombre no este duplicado"
		apostadores= [elem.__dict__ for elem in self.session.query(Apostador).all()]
		apostador_random=random.choice(apostadores)
		validacion=self.logica.validar_crear_editar_apostador(apostador_random["Nombre"])
		self.assertEqual(validacion, "El nombre ya existe")
		

	def test_validar_crear_editar_apostador_string(self):
		"HU006 se valida que el nombre sea un String"
		validacion=self.logica.validar_crear_editar_apostador("12345")
		print(validacion)
		self.assertEqual(validacion, "El nombre contiene numeros")

	def test_dar_apuestas_carrera_vacio(self):
		"HU011 Se valida que liste vacio"
		self.skip_setUp = True
		self.session.query(Apuesta).delete()
		self.session.query(Apostador).delete()
		self.session.commit()
		self.session.close
		consulta = self.logica.dar_apuestas_carrera(random.randint(1,7))
		self.assertEqual(len(consulta),0)
		
	def test_dar_apuestas_carrera(self):
		"HU011 se valida que liste dar apuestas con las 21 cargadas en el setUp"
		lista=self.logica.dar_apuestas_carrera(1)
		self.assertEqual(len(lista),21)
   
	@unittest.skip("Test aprovado") 
	def test_crear_apuesta_mayor_0_valor_apuesta(self):
		"HUO12 crear apuesta con valor mayor a cero"
		idCar,idCom,idApos = consulta_aleatoria(self)
		valor = round(random.uniform(0, 100), 2)
		apuestas = [elem.__dict__ for elem in self.session.query(Apuesta).all()]
		len_apuesta = len(apuestas)
		self.logica.crear_apuesta(self.apostadores[idApos].Nombre, self.carreras[idCar].id, valor, self.competidores[idCom].Nombre)
		apuestas_2 = [elem.__dict__ for elem in self.session.query(Apuesta).all()]
		test = apuestas_2[len_apuesta]["Valor"]
		self.assertGreater(test,0)

	@unittest.skip("Test aprovado")
	def test_crear_apuesta_no_vacio_valor_apuesta(self):
		"HUO12 crear apuesta no vacia"
		idCar,idCom,idApos = consulta_aleatoria(self)
		valor = round(random.uniform(0, 100), 2)
		apuestas = [elem.__dict__ for elem in self.session.query(Apuesta).all()]
		len_apuesta = len(apuestas)
		self.logica.crear_apuesta(self.apostadores[idApos].Nombre, self.carreras[idCar].id, valor, self.competidores[idCom].Nombre)
		apuestas_2 = [elem.__dict__ for elem in self.session.query(Apuesta).all()]
		test = apuestas_2[len_apuesta]["Valor"]
		self.assertIsNotNone(test)

	@unittest.skip("Test aprovado")
	def test_crear_apuesta_valor_tipo_float(self):
		"HUO12 crear apuesta con valor float"
		idCar,idCom,idApos = consulta_aleatoria(self)
		valor = round(random.uniform(0, 100), 2)
		apuestas = [elem.__dict__ for elem in self.session.query(Apuesta).all()]
		len_apuesta = len(apuestas)
		self.logica.crear_apuesta(self.apostadores[idApos].Nombre, self.carreras[idCar].id, valor, self.competidores[idCom-1].Nombre)
		apuestas_2 = [elem.__dict__ for elem in self.session.query(Apuesta).all()]
		test = apuestas_2[len_apuesta]["Valor"]
		self.assertTrue(validar_float(test))

	@unittest.skip("Test verificado")
	def test_terminar_carrera(self):
		"HU003 test terminar carrera verificar cambio de estado"
		total_carreras=self.session.query(Carrera).count()
		print("Total_ccarreras", total_carreras)
		id_random=random.randint(1,int(total_carreras))
		self.logica.terminar_carrera(id_random,1)
		consulta2=self.session.query(Carrera).filter_by(id=id_random).first()

		self.assertFalse(consulta2.Abierta, False)

    # #HU014
	@unittest.skip("Test verificado")   
	def test_dar_reporte_ganancias_ver_nombre_apostadores(self):
		"HU014 test dar reporte ganancias ver nombre apostadores"
		idCar,idCom,idApos = consulta_aleatoria(self)
		consultaGA, consultaGC = self.logica.dar_reporte_ganancias(self.carreras[idCar].id,self.competidores[idCom].id) #GA = ganancias apostador GC= ganancias casa
		self.assertTrue(validar_nombres_no_vacios(consultaGA))

	@unittest.skip("Test verificado")
	def test_dar_reporte_ganancias_ver_nombre_apostadores_no_none(self):
		"HU014 test dar reporte ganancias ver nombre apostadores no none"
		idCar,idCom,idApos = consulta_aleatoria(self)
		consultaGA, consultaGC = self.logica.dar_reporte_ganancias(self.carreras[idCar].id,self.competidores[idCom].id) #GA = ganancias apostador GC= ganancias casa
		self.assertTrue(validar_ganancias_no_none(consultaGA))

	@unittest.skip("Test verificado")	
	def test_dar_reporte_ganancias_ganancias_casa(self):
		"HU014 test dar reporte ganancias de la casa"
		idCar,idCom,idApos = consulta_aleatoria(self)
		consultaGA, consultaGC = self.logica.dar_reporte_ganancias(self.carreras[idCar].id,self.competidores[idCom].id) #GA = ganancias apostador GC= ganancias casa
		self.assertTrue(validar_ganancias_casa_no_none(consultaGC))
		
	@unittest.skip("Test verificado")	
	def test_dar_reporte_ganancias_calcularganancias(self):
		"HU014 test dar reporte ganancias calculo de ganacias"
		self.session.query(Competidor).delete()
		self.session.query(Carrera).delete()
		self.session.query(Apostador).delete()
		self.session.query(Apuesta).delete()
		self.session.commit()
		self.session.close
		#se crea carrera
		crear_modelo_ganancias(self)
		consultaGA, consultaGC = self.logica.dar_reporte_ganancias(0,2)
		gananciaApos = 16.67
		gananciaCasa = 93.33

		testCasa = False
		testapost = False 
		if abs(gananciaCasa) == abs(consultaGC):
			testCasa = True

		for i in consultaGA:
			consultaGAv = i[1]
			if abs(consultaGAv) == abs(gananciaApos):
				testapost = True 

		self.assertTrue(testCasa)
		self.assertTrue(testapost)

	def test_validar_crear_apuesta_apostador_vacio(self):
		"HU012 test validar crear apuestas apostador vacio"
		carreras= [elem.__dict__ for elem in self.session.query(Carrera).all()]
		carrera_random=random.choice(carreras)
		carrera_nombre=carrera_random["Nombre"]
		competidores = [elem.__dict__ for elem in self.session.query(Competidor).filter_by(carrera_id=carrera_random["id"]).all()]
		competidor_random = random.choice(competidores)
		Valor=self.data_factory.pyfloat(min_value=1, max_value=100, right_digits=2)
		validacion = self.logica.validar_crear_editar_apuesta("",carrera_nombre,Valor, competidor_random["Nombre"])
		self.assertEqual(validacion, "Debe seleccionar un apostador")
    
	def test_validar_crear_apuesta_competidor_vacio(self):
		"HU012 test validar crear apuestas competidor vacio"
		carreras= [elem.__dict__ for elem in self.session.query(Carrera).all()]
		carrera_random=random.choice(carreras)
		carrera_nombre=carrera_random["Nombre"]
		apostadores= [elem.__dict__ for elem in self.session.query(Apostador).all()]
		apostador_random=random.choice(apostadores)
		Valor=self.data_factory.pyfloat(min_value=1, max_value=100, right_digits=2)
		validacion = self.logica.validar_crear_editar_apuesta(apostador_random["Nombre"],carrera_nombre,Valor,"")
		self.assertEqual(validacion, "Debe seleccionar un competidor")

	def test_valor_vacio(self):
		"HU012 test validar crear apuestas valor vacio"
		carreras= [elem.__dict__ for elem in self.session.query(Carrera).all()]
		carrera_random=random.choice(carreras)
		carrera_nombre=carrera_random["Nombre"]
		competidores = [elem.__dict__ for elem in self.session.query(Competidor).filter_by(carrera_id=carrera_random["id"]).all()]
		competidor_random = random.choice(competidores)
		apostadores= [elem.__dict__ for elem in self.session.query(Apostador).all()]
		apostador_random=random.choice(apostadores)
		validacion = self.logica.validar_crear_editar_apuesta(apostador_random["Nombre"],carrera_nombre,"",competidor_random["Nombre"])
		self.assertEqual(validacion, "El campo Valor Apuesta no debe estar vacío")

	def test_valor_no_numerico(self):
		"HU012 test validar crear apuestas valor no numerico"
		carreras= [elem.__dict__ for elem in self.session.query(Carrera).all()]
		carrera_random=random.choice(carreras)
		carrera_nombre=carrera_random["Nombre"]
		competidores = [elem.__dict__ for elem in self.session.query(Competidor).filter_by(carrera_id=carrera_random["id"]).all()]
		competidor_random = random.choice(competidores)
		apostadores= [elem.__dict__ for elem in self.session.query(Apostador).all()]
		apostador_random=random.choice(apostadores)
		validacion = self.logica.validar_crear_editar_apuesta(apostador_random["Nombre"],carrera_nombre,"strkjl",competidor_random["Nombre"])
		self.assertEqual(validacion, "El campo Valor Apuesta debe ser un número válido")