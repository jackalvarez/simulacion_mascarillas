import random
from distribution import Distribution, Uniform, DirectNormal, ConvolutionNormal, Exponential, DensityFunction
from mask import Mask
from employee import Employee, EmployeeSection1, EmployeeSection2

"""
	Clase donde se ejecuta cada corrida de la simulación.
	Aquí se llevan a cabo los seis eventos definidos:
		- L1: Llegada de máscaras a la sección 1 por medio externos al sistema.
		- D: Desinfección de una máscara por el encargado de la sección 1.
		- L1S2: Llegada de máscaras a la sección 1 que fueron devueltas en la sección 2.
		- L2: Llegada de máscaras a la sección 2 desde la sección 1.
		- E1: Empaquetado de pares de máscaras por el encargado 1 de la sección 2.
		- E1: Empaquetado de pares de máscaras por el encargado 2 de la sección 2.

	Además, en esta clase se lleva el acumulado de tiempos de servicio, 
	que pasa una máscara en el sistema antes de ser botada, destruida o empaquetada.

	Lleva control del tiempo, para que la simulación solo se ejecute por el tiempo definido por el usuario.
"""
class Simulation:
	def __init__(self, simNumber, maxTime, D1, D2, D3, D4):
		self.warm_up_time = 120
		
		self.simNumber = simNumber
		self.maxTime = maxTime
		
		self.clock = 0.0

		# Eventos
		self.events = {
					"L1": 0.0, 
					"D": self.maxTime, 
					"L1S2": self.maxTime,
					"L2": self.maxTime,
					"E1": self.maxTime,
					"E2": self.maxTime
					}

		# Encargados
		self.encargado_s1 = EmployeeSection1(self.warm_up_time)
		self.encargado_s2a = EmployeeSection2(self.warm_up_time)
		self.encargado_s2b = EmployeeSection2(self.warm_up_time)

		# Colas en cada en sección
		self.colaEsperaDesinfeccion = []
		self.colaEsperaEmpaquetado = []

		# Colas de arribos entre secciones
		self.section1Queue = []
		self.section2Queue = []

		# Distribuciones
		self.D1 = D1
		self.D2 = D2
		self.D3 = D3
		self.D4 = D4

		# Para la generación de valores para casos en que se bota la máscara o se manda a desinfectar de nuevo, etc.
		self.distribucion_uniforme = Uniform(0,1)

		# Tiempos acumulativos de mascarillas
		self.acum_servicio = 0
		self.acum_empaquetadas = 0
		self.acum_destruidas = 0
		self.acum_botadas = 0

		# Cantidad de mascarillas que llegaron al sistema
		self.llegadas = 0

		# Contadores para saber cómo salieron mascarillas del sistema
		self.empaquetadas = 0
		self.destruidas = 0
		self.botadas = 0

	# Evento de cuando llega una mascarilla a la sección 1
	def event_l1(self):
		# Se agrega 1 al contador de mascarillas que han entrado al sistema
		if self.clock > self.warm_up_time:
			self.llegadas += 1

		mask = Mask(self.clock)

		if self.encargado_s1.disponible:
			# Genera tiempo de desinfección
			self.encargado_s1.set_current_mask(self.clock, mask)
			self.events["D"] = self.clock + self.D2.generate_random_value()
			
		else:
			self.colaEsperaDesinfeccion.append(mask)
		# Genera tiempo de arribo para siguiente mascarilla
		self.events["L1"] = self.clock + self.D1.generate_random_value()

	# Evento de desinfección de una mascarilla
	def event_d(self):
		mask = self.encargado_s1.mask
		self.encargado_s1.service_ends(self.clock)
		salida_mascara = self.distribucion_uniforme.generate_random_value()
		if salida_mascara < 0.9:
			t_llegada_s2 = self.clock + 1
			self.section2Queue.append((t_llegada_s2, mask))
			if self.events["L2"] == self.maxTime:
				self.events["L2"], mask = self.section2Queue[0]
		else:
			# Se destruye la máscara
			if mask.init_time > self.warm_up_time:
				self.destruidas += 1
				self.acum_destruidas += self.clock - mask.init_time
				self.acum_servicio += mask.cumulative_service_time
			del mask
		if len(self.colaEsperaDesinfeccion) > 0:
			mask = self.colaEsperaDesinfeccion.pop(0)
			self.encargado_s1.set_current_mask(self.clock, mask)
			# Genera tiempo de desinfección
			self.events["D"] = self.clock + self.D2.generate_random_value()
		else:
			self.events["D"] = self.maxTime
	
	# Evento de llegada de un par de mascarillas a sección 1 desde sección 2
	def event_l1s2(self):
		_, mask1, mask2 = self.section1Queue.pop(0)
		if self.encargado_s1.disponible:
			self.encargado_s1.set_current_mask(self.clock, mask1)
			self.colaEsperaDesinfeccion.append(mask2)
			# Genera tiempo de desinfección
			self.events["D"] = self.clock + self.D2.generate_random_value()
		else:
			self.colaEsperaDesinfeccion.append(mask1)
			self.colaEsperaDesinfeccion.append(mask2)

		if len(self.section1Queue) > 0:
			self.events["L1S2"], mask1, mask2 = self.section1Queue[0]
		else:
			self.events["L1S2"] = self.maxTime

	# Evento de llegada de mascarilla a sección 2
	def event_l2(self):
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
				self.events["E1"] = self.clock + self.D3.generate_random_value()
			elif encargado_elegido == 2:
				self.encargado_s2b.set_current_masks(self.clock, mask1, mask2)
				# Genera valor para tiempo de servicio de encargado 2
				self.events["E2"] = self.clock + self.D4.generate_random_value()
		if len(self.section2Queue) > 0:
			self.events["L2"], mask = self.section2Queue[0]
		else:
			self.events["L2"] = self.maxTime

	# Evento de un par de mascarillas empaquetadas por el encargado 1
	def event_e1(self):
		mask1 = self.encargado_s2a.mask1
		mask2 = self.encargado_s2a.mask2
		self.encargado_s2a.service_ends(self.clock)
		destino_mascarilla = self.distribucion_uniforme.generate_random_value()
		if destino_mascarilla < 0.05:
			# Se botan las dos mascarillas
			if mask1.init_time > self.warm_up_time:
				self.botadas += 1
				self.acum_botadas += self.clock - mask1.init_time
				self.acum_servicio += mask1.cumulative_service_time
			if mask2.init_time > self.warm_up_time:
				self.botadas += 1
				self.acum_botadas += self.clock - mask2.init_time
				self.acum_servicio += mask2.cumulative_service_time
			del mask1
			del mask2
		elif 0.05 <= destino_mascarilla and destino_mascarilla < 0.25:
			# Se mandan a desinfectar de nuevo
			llegada = self.clock + 2
			self.section1Queue.append((llegada, mask1, mask2))
			if self.events["L1S2"] == self.maxTime:
				self.events["L1S2"], mask1, mask2 = self.section1Queue[0]
		else:
			# Se logran empaquetar y salen del sistema
			if mask1.init_time > self.warm_up_time:
				self.empaquetadas += 1
				self.acum_empaquetadas += self.clock - mask1.init_time
				self.acum_servicio += mask1.cumulative_service_time
			if mask2.init_time > self.warm_up_time:
				self.empaquetadas += 1
				self.acum_empaquetadas += self.clock - mask2.init_time
				self.acum_servicio += mask2.cumulative_service_time
			del mask1
			del mask2
		if len(self.colaEsperaEmpaquetado) > 1:
			mask1 = self.colaEsperaEmpaquetado.pop(0)
			mask2 = self.colaEsperaEmpaquetado.pop(0)
			self.encargado_s2a.set_current_masks(self.clock, mask1, mask2)
			# Genera valor para tiempo de servicio de encargado 1
			self.events["E1"] = self.clock + self.D3.generate_random_value()
		else:
			self.events["E1"] = self.maxTime

	# Evento de un par de mascarillas empaquetadas por el encargado 1
	def event_e2(self):
		mask1 = self.encargado_s2b.mask1
		mask2 = self.encargado_s2b.mask2
		self.encargado_s2b.service_ends(self.clock)
		destino_mascarilla = self.distribucion_uniforme.generate_random_value()
		if destino_mascarilla < 0.15:
			# Se botan las dos mascarillas
			if mask1.init_time > self.warm_up_time:
				self.botadas += 1
				self.acum_botadas += self.clock - mask1.init_time
				self.acum_servicio += mask1.cumulative_service_time
			if mask2.init_time > self.warm_up_time:
				self.botadas += 1
				self.acum_botadas += self.clock - mask2.init_time
				self.acum_servicio += mask2.cumulative_service_time
			del mask1
			del mask2
		elif 0.15 <= destino_mascarilla and destino_mascarilla < 0.4:
			# Se mandan a desinfectar de nuevo
			llegada = self.clock + 2
			self.section1Queue.append((llegada, mask1, mask2))
			if self.events["L1S2"] == self.maxTime:
				self.events["L1S2"], _, _ = self.section1Queue[0]
		else:
			# Se logran empaquetar y salen del sistema
			if mask1.init_time > self.warm_up_time:
				self.empaquetadas += 1
				self.acum_empaquetadas += self.clock - mask1.init_time
				self.acum_servicio += mask1.cumulative_service_time
			if mask2.init_time > self.warm_up_time:
				self.empaquetadas += 1
				self.acum_empaquetadas += self.clock - mask2.init_time
				self.acum_servicio += mask2.cumulative_service_time
			del mask1
			del mask2
		if len(self.colaEsperaEmpaquetado) > 1:
			mask1 = self.colaEsperaEmpaquetado.pop(0)
			mask2 = self.colaEsperaEmpaquetado.pop(0)
			self.encargado_s2b.set_current_masks(self.clock, mask1, mask2)
			# Genera valor para tiempo de servicio de encargado 1
			self.events["E2"] = self.clock + self.D3.generate_random_value()
		else:
			self.events["E2"] = self.maxTime

	def run(self):
		while self.clock < self.maxTime:
			# El reloj se actualiza dentro de cada evento, entonces siempre se ejecutaba un evento de más
			event = self.min_event()
			self.clock = self.events[event]
			if self.clock < self.maxTime:
				#print(str(self.clock) + ": " + event )
				if event == "L1":
					self.event_l1()
					#print("Reloj: " + str(self.clock))
				elif event == "D":
					self.event_d()
				elif event == "L1S2":
					self.event_l1s2()
				elif event == "L2":
					self.event_l2()
				elif event == "E1":
					self.event_e1()
				else:
					self.event_e2()

	# Método para obtener valores necesarios para las estadísticas promedio de todas las corridas. Se obtienen valores como
	# el total de máscaras que se destruyeron o botaron, el total de máscaras que salieron y acumulados de tiempos de máscaras.
	def getStatistics(self):
		masks_lost = self.botadas + self.destruidas
		total_masks = masks_lost + self.empaquetadas 
		lost_masks_time = self.acum_botadas + self.acum_destruidas
		total_mask_time = lost_masks_time + self.acum_empaquetadas
		total_mask_time = lost_masks_time + self.acum_empaquetadas

		return self.botadas, self.destruidas, self.empaquetadas, self.acum_botadas, self.acum_destruidas, self.acum_empaquetadas, self.acum_servicio, self.clock-self.warm_up_time, self.section1Queue, self.section2Queue, self.llegadas, self.encargado_s1.acum_service_time, self.encargado_s2a.acum_service_time, self.encargado_s2b.acum_service_time, total_mask_time / total_masks

	# Método que obtiene el evento con la programación mínima, es decir, que está más pronto a ocurrir.
	def min_event(self):
		return min(self.events, key=self.events.get)
		
	# Método que imprime las estadísticas de la corrida en particular.
	def print_statistics(self):
		masks_lost = self.botadas + self.destruidas
		total_masks = masks_lost + self.empaquetadas 
		lost_masks_time = self.acum_botadas + self.acum_destruidas
		total_mask_time = lost_masks_time + self.acum_empaquetadas
		mean_service_time = self.acum_servicio / total_masks

		stable_system_time = self.clock - self.warm_up_time

		print("\n\n------------ESTADÍSTICAS DE LA SIMULACIÓN " + str(self.simNumber + 1) + "------------\n")
		print("Tiempo que corrieron las simulaciones: " + str(round(stable_system_time,2)) + " minutos" )
		print("Longitud de la cola en sección 1: " + str(len(self.section1Queue)) )
		print("Longitud de la cola en sección 2: " + str(len(self.section2Queue)) )
		print("Tiempo promedio que pasa una mascarilla en el sistema antes de botarse o destruirse: " + str(round(lost_masks_time/masks_lost,2)) + " minutos")
		print("Tiempo promedio que pasa una mascarilla en el sistema antes de empaquetarse: " + str(round(self.acum_empaquetadas/self.empaquetadas,2)) + " minutos")
		print("Tiempo promedio que pasa una mascarilla en el sistema en general: " + str(round(total_mask_time/total_masks,2)) + " minutos") 
		print("Tiempo promedio de servicio para una mascarilla en el sistema en general: " + str(round(mean_service_time,2)) + " minutos") 
		print("Eficiencia del sistema (Ws/W): " + str( round(mean_service_time / total_mask_time * total_masks, 2)))
		print("Equilibrio del sistema: " + str( round(self.llegadas / total_masks,2) ) )
		print("Total de máscaras que llegaron: " + str(self.llegadas))
		print("\tTotal de máscaras que se botaron (o destruyeron): " + str(masks_lost) + " (" + str(round(masks_lost/self.llegadas * 100, 2)) + "%)")
		print("\tTotal de máscaras que se empacaron: " + str(self.empaquetadas) + " (" + str(round(self.empaquetadas/self.llegadas * 100, 2)) + "%)")
		print("Porcentaje de tiempo real de trabajo de los empleados:")
		print("\tEmpleado de sección 1: " + str(round(self.encargado_s1.acum_service_time / self.clock, 2)) )
		print("\tEmpleado 1 de sección 2: " + str(round(self.encargado_s2a.acum_service_time / self.clock, 2)) )
		print("\tEmpleado 2 de sección 2: " + str(round(self.encargado_s2b.acum_service_time / self.clock, 2)) )