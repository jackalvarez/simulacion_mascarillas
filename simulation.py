import random
from distribution import Distribution, Uniform, DirectNormal, ConvolutionNormal, Exponential, DensityFunction
from mask import Mask
from employee import Employee, EmployeeSection1, EmployeeSection2

class Simulation:
	def __init__(self, maxTime):
		self.maxTime = maxTime
		
		self.clock = 0
		self.L1 = 0
		self.D = maxTime
		self.L1S2 = maxTime
		self.L2 = maxTime
		self.E1 = maxTime
		self.E2 = maxTime
		self.encargado_s1 = EmployeeSection1()
		self.encargado_s2a = EmployeeSection2()
		self.encargado_s2b = EmployeeSection2()

		self.colaEsperaDesinfeccion = []
		self.colaEsperaEmpaquetado = []

		self.section1Queue = []
		self.section2Queue = []

		# Distribuciones
		self.D1 = Distribution()
		self.D2 = Distribution()
		self.D3 = Distribution()
		self.D4 = Distribution()

		# Para la generación de valores para casos de botar máscara y así
		self.distribucion_uniforme = Uniform(0,1)

		# Tiempos acumulativos de mascarillas
		self.acum_empaquetadas = 0
		self.acum_destruidas = 0
		self.acum_botadas = 0

		# Contadores para saber cómo salieron mascarillas del sistema
		self.empaquetadas = 0
		self.destruidas = 0
		self.botadas = 0

	# Arrival of a mask to section 1
	def event_l1(self):
		self.clock = self.L1
		mask = Mask(self.clock)

		if self.encargado_s1.disponible:
			# Genera tiempo de desinfección
			self.encargado_s1.set_current_mask(self.clock, mask)
			self.D = self.clock + self.D2.generate_random_value()
		else:
			self.colaEsperaDesinfeccion.append(mask)
		# Genera tiempo de arribo para siguiente mascarilla
		self.L1 = self.clock + self.D1.generate_random_value()

	def event_d(self):
		self.clock = self.D
		mask = self.encargado_s1.mask
		self.encargado_s1.service_ends(self.clock)
		salida_mascara = self.distribucion_uniforme.generate_random_value()
		if salida_mascara < 0.9:
			t_llegada_s2 = self.clock + 1
			self.section2Queue.append((t_llegada_s2, mask))
			if self.L2 == self.maxTime:
				self.L2, mask = self.section2Queue[0]
		else:
			# Se destruye la máscara
			self.destruidas += 1
			self.acum_destruidas += self.clock - mask.init_time
			del mask
		if len(self.colaEsperaDesinfeccion) > 0:
			mask = self.colaEsperaDesinfeccion.pop(0)
			self.encargado_s1.set_current_mask(self.clock, mask)
			# Genera tiempo de desinfección
			self.D = self.clock + self.D2.generate_random_value()
		else:
			self.D = self.maxTime
	
	def event_l1s2(self):
		self.clock = self.L1S2
		_, mask1, mask2 = self.section1Queue.pop(0)
		if self.encargado_s1.disponible:
			self.encargado_s1.set_current_mask(self.clock, mask1)
			self.colaEsperaDesinfeccion.append(mask2)
			# Genera tiempo de desinfección
			self.D = self.clock + self.D2.generate_random_value()
		else:
			self.colaEsperaDesinfeccion.append(mask1)
			self.colaEsperaDesinfeccion.append(mask2)

		if len(self.section1Queue) > 0:
			self.L1S2, mask1, mask2 = self.section1Queue[0]
		else:
			self.L1S2 = self.maxTime

	def event_l2(self):
		self.clock = self.L2
		_, mask = self.section2Queue.pop(0)
		self.colaEsperaEmpaquetado.append(mask)
		if len(self.colaEsperaEmpaquetado) > 1 and (self.encargado_s2a.disponible or self.encargado_s2b.disponible):
			mask1 = self.colaEsperaEmpaquetado.pop(0)
			mask2 = self.colaEsperaEmpaquetado.pop(0)
			encargado_elegido = 0
			if self.encargado_s2a.disponible and self.encargado_s2b.disponible:
				probabilidad_de_encargado = self.distribucion_uniforme.generate_random_value()
				if probabilidad_de_encargado < 0.5:
					encargado_elegido = 1
				else:
					encargado_elegido = 2
			elif self.encargado_s2a.disponible:
				encargado_elegido = 1
			else:
				encargado_elegido = 2
			
			if encargado_elegido == 1:
				self.encargado_s2a.set_current_masks(self.clock, mask1, mask2)
				# Genera valor para tiempo de servicio de encargado 1
				self.E1 = self.clock + self.D3.generate_random_value()
			elif encargado_elegido == 2:
				self.encargado_s2b.set_current_masks(self.clock, mask1, mask2)
				# Genera valor para tiempo de servicio de encargado 2
				self.E2 = self.clock + self.D4.generate_random_value()
		if len(self.section2Queue) > 0:
			self.L2, mask = self.section2Queue[0]
		else:
			self.L2 = self.maxTime

	def event_e1(self):
		self.clock = self.E1
		mask1 = self.encargado_s2a.mask1
		mask2 = self.encargado_s2a.mask2
		self.encargado_s2a.service_ends(self.clock)
		destino_mascarilla = self.distribucion_uniforme.generate_random_value()
		if destino_mascarilla < 0.05:
			# Se botan las dos mascarillas
			self.botadas += 2
			self.acum_botadas += (self.clock - mask1.init_time) + (self.clock - mask2.init_time)
			del mask1
			del mask2
		elif 0.05 <= destino_mascarilla and destino_mascarilla < 0.25:
			# Se mandan a desinfectar de nuevo
			llegada = self.clock + 2
			self.section1Queue.append((llegada, mask1, mask2))
			if self.L1S2 == self.maxTime:
				self.L1S2, mask1, mask2 = self.section1Queue[0]
		else:
			# Se logran empaquetar y salen del sistema
			self.empaquetadas += 2
			self.acum_empaquetadas += (self.clock - mask1.init_time) + (self.clock - mask2.init_time)
			del mask1
			del mask2
		if len(self.colaEsperaEmpaquetado) > 1:
			mask1 = self.colaEsperaEmpaquetado.pop(0)
			mask2 = self.colaEsperaEmpaquetado.pop(0)
			self.encargado_s2a.set_current_masks(self.clock, mask1, mask2)
			# Genera valor para tiempo de servicio de encargado 1
			self.E1 = self.clock + self.D3.generate_random_value()
		else:
			self.E1 = self.maxTime

	def event_e2(self):
		self.clock = self.E2
		mask1 = self.encargado_s2b.mask1
		mask2 = self.encargado_s2b.mask2
		self.encargado_s2b.service_ends(self.clock)
		destino_mascarilla = self.distribucion_uniforme.generate_random_value()
		if destino_mascarilla < 0.15:
			# Se botan las dos mascarillas
			self.botadas += 2
			self.acum_botadas += (self.clock - mask1.init_time) + (self.clock - mask2.init_time)
			del mask1
			del mask2
		elif 0.15 <= destino_mascarilla and destino_mascarilla < 0.4:
			# Se mandan a desinfectar de nuevo
			llegada = self.clock + 2
			self.section1Queue.append((llegada, mask1, mask2))
			if self.L1S2 == self.maxTime:
				self.L1S2, mask1, mask2 = self.section1Queue[0]
		else:
			# Se logran empaquetar y salen del sistema
			self.empaquetadas += 2
			self.acum_empaquetadas += (self.clock - mask1.init_time) + (self.clock - mask2.init_time)
			del mask1
			del mask2
		if len(self.colaEsperaEmpaquetado) > 1:
			mask1 = self.colaEsperaEmpaquetado.pop(0)
			mask2 = self.colaEsperaEmpaquetado.pop(0)
			self.encargado_s2b.set_current_masks(self.clock, mask1, mask2)
			# Genera valor para tiempo de servicio de encargado 1
			self.E2 = self.clock + self.D3.generate_random_value()
		else:
			self.E2 = self.maxTime

	