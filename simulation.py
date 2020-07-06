import random
from distribution import Distribution, Uniform, DirectNormal, ConvolutionNormal, Exponential, DensityFunction

class Simulation:
	def __init__(self, repetitions, maxTime):
		self.repetitions = repetitions
		self.maxTime = maxTime
		
		self.reloj = 0
		self.L1 = 0
		self.D = maxTime
		self.L1S2 = maxTime
		self.L2 = maxTime
		self.E1 = maxTime
		self.E2 = maxTime
		self.encargado1Disponible = True
		self.encargado2aDisponible = True
		self.encargado2bDisponible = True

		self.colaEsperaDesinfeccion = 0
		self.colaEsperaEmpaquetado = 0

		self.section1Queue = []
		self.section2Queue = []

		# Distribuciones
		self.D1 = Distribution()
		self.D2 = Distribution()
		self.D3 = Distribution()
		self.D4 = Distribution()

		# Para la generación de valores para casos de botar máscara y así
		self.distribucion_uniforme = Uniform(0,1)

	# Arrival of a mask to section 1
	def event_l1(self):
		self.clock = self.L1

		if self.encargado1Disponible:
			# Genera tiempo de desinfección
			self.D = self.clock + self.D2.generate_random_value()
		else:
			self.colaEsperaDesinfeccion += 1
		# Genera tiempo de arribo para siguiente mascarilla
		self.L1 = self.clock + self.D1.generate_random_value()

	def event_d(self):
		self.clock = self.D
		salida_mascara = self.distribucion_uniforme.generate_random_value()
		if salida_mascara < 0.9:
			t_llegada_s2 = self.clock + 1
			self.section2Queue.append(t_llegada_s2)
			if self.L2 == self.maxTime:
				self.L2 = self.section2Queue[0]
		else:
			# Destruye mascarilla
			# Aquí es donde se aumentan los contadores para estadísticas
			1 == 1
		if self.colaEsperaDesinfeccion > 0:
			# Genera tiempo de desinfección
			self.D = self.clock + self.D2.generate_random_value()
			self.colaEsperaDesinfeccion -= 1
		else:
			self.D = self.maxTime
	
	def event_l1s2(self):
		self.clock = self.L1S2
		self.section1Queue.remove(self.L1S2)
		if self.encargado1Disponible:
			self.encargado1Disponible = False
			self.colaEsperaDesinfeccion += 1
			# Genera tiempo de desinfección
			self.D = self.clock + self.D2.generate_random_value()
		else:
			self.colaEsperaDesinfeccion += 2

		if len(self.section1Queue) > 0:
			self.L1S2 = self.section1Queue[0]
		else:
			self.L1S2 = self.maxTime

	def event_l2(self):
		self.clock = self.L2
		self.section2Queue.remove(self.L2)
		self.colaEsperaEmpaquetado += 1
		if self.colaEsperaEmpaquetado > 1 and (self.encargado2aDisponible or self.encargado2bDisponible):
			self.colaEsperaEmpaquetado -= 2
			encargado_elegido = 0
			if self.encargado2aDisponible and self.encargado2bDisponible:
				probabilidad_de_encargado = self.distribucion_uniforme.generate_random_value()
				if probabilidad_de_encargado < 0.5:
					encargado_elegido = 1
				else:
					encargado_elegido = 2
			elif self.encargado1Disponible:
				encargado_elegido = 1
			else:
				encargado_elegido = 2
			
			if encargado_elegido == 1:
				# Genera valor para tiempo de servicio de encargado 1
				self.E1 = self.clock + self.D3.generate_random_value()
			elif encargado_elegido == 2:
				# Genera valor para tiempo de servicio de encargado 2
				self.E2 = self.clock + self.D4.generate_random_value()
		if len(self.section2Queue) > 0:
			self.L2 = self.section2Queue[0]
		else:
			self.L2 = self.maxTime

	def event_e1(self):
		self.clock = self.E1
		destino_mascarilla = self.distribucion_uniforme.generate_random_value()
		if destino_mascarilla < 0.05:
			# Se botan las dos mascarillas
			1 == 1
		elif 0.05 <= destino_mascarilla and destino_mascarilla < 0.25:
			# Se mandan a desinfectar de nuevo
			llegada = self.clock + 2
			self.section1Queue.append(llegada)
			if self.L1S2 == self.maxTime:
				self.L1S2 = self.section1Queue[0]
		else:
			# Se logran empaquetar y salen del sistema
			1 == 1
		if self.colaEsperaEmpaquetado > 1:
			self.colaEsperaDesinfeccion -= 2
			# Genera valor para tiempo de servicio de encargado 1
			self.E1 = self.clock + self.D3.generate_random_value()
		else:
			self.E1 = self.maxTime

	def event_e2(self):
		self.clock = self.E2
		destino_mascarilla = self.distribucion_uniforme.generate_random_value()
		if destino_mascarilla < 0.15:
			# Se botan las dos mascarillas
			1 == 1
		elif 0.15 <= destino_mascarilla and destino_mascarilla < 0.4:
			# Se mandan a desinfectar de nuevo
			llegada = self.clock + 2
			self.section1Queue.append(llegada)
			if self.L1S2 == self.maxTime:
				self.L1S2 = self.section1Queue[0]
		else:
			# Se logran empaquetar y salen del sistema
			1 == 1
		if self.colaEsperaEmpaquetado > 1:
			self.colaEsperaDesinfeccion -= 2
			# Genera valor para tiempo de servicio de encargado 1
			self.E2 = self.clock + self.D4.generate_random_value()
		else:
			self.E2 = self.maxTime


	def start(self):
		print('Inicia la simulación')
		# Aquí hay que hacer el ciclo principal y eso

	def read_distributions(self):
		print('Considere las siguientes distribuciones:')
		print('\ta) distribución uniforme en (a,b)')
		print('\tb) distribución normal - método directo')
		print('\tc) distribución normal - método de la convolución')
		print('\td) distribución exponencial parámetro lambda')
		print('\te) distribución con función de densidad: f(x) = kx')

	def print_statistics(self):
		print('Aquí algún día van a ir estadísticas')

	def generate_random_value(self, distribution):
		print('Esto la verdad no sé cómo implementarlo todavía :v')
		return random.random()

	