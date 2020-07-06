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
			self.D = self.clock + self.D2.generate_random_value()
		else:
			self.colaEsperaDesinfeccion += 1

		self.L1 = self.clock + self.D1.generate_random_value()

	def event_d(self):
		self.clock = self.D



	def start(self):
		print('Inicia la simulación')
		self.event_l1()

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

	