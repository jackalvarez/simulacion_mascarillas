from distribution import Distribution, Uniform, DirectNormal, ConvolutionNormal, Exponential, DensityFunction
from simulation import Simulation

class SimulationManager:
    def __init__(self, repetitions, maxTime):
        self.repetitions = repetitions
        self.maxTime = maxTime

        self.totalRunTime = 0
        
        self.totalQueueSizeSection1 = 0
        self.totalQueueSizeSection2 = 0
        
        # Distribuciones
        self.distributions = []

        # Datos para las estadísticas
        self.clock = 0
        self.section1QueueSize = 0
        self.section2QueueSize = 0

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

        # Encargados
        self.employee1Time = 0
        self.employee2Time = 0
        self.employee3Time = 0
        
    def distribution_factory(self, choice):
        if (choice == 'a'):
            return Uniform()
        if (choice == 'b'):
            return DirectNormal()
        if (choice == 'c'):
            return ConvolutionNormal()
        if (choice == 'd'):
            return Exponential()
        if (choice == 'e'):
            return DensityFunction()
        
        return None
        
    def read_distributions(self):
        print('Considere las siguientes distribuciones:')
        print('\ta) distribución uniforme en (a,b)')
        print('\tb) distribución normal - método directo')
        print('\tc) distribución normal - método de la convolución')
        print('\td) distribución exponencial parámetro lambda')
        print('\te) distribución con función de densidad: f(x) = kx')
        
        for i in range(4):
            print('\n')
            choice = input('\tPor favor digite la letra [a-e] de la distribución que desea para D' + str(i) + ': ')
            self.distributions.append( self.distribution_factory(choice))

            if self.distributions[i] is not None:
                self.distributions[i].read_distribution()
    
    # Este método es el que toma los datos de cada una de las simulaciones, cada vez que estas terminan de ejecutar
    # Toma los datos que devuelven las demás simulaciones, y se los suma a los contadores actuales
    def get_sim_stats(self, sim):
        # Se llama al método getStatistics(), que devuelve todos los valores de la simulación
        botadas, destruidas, empaquetadas, acum_botadas, acum_destruidas, acum_empaquetadas, acum_servicio, clock, section1Queue, section2Queue, llegadas, employee1Time, employee2Time, employee3Time = sim.getStatistics()
        
        # Se asignan todos los valores a las variables totales
        self.botadas += botadas
        self.destruidas += destruidas
        self.empaquetadas += empaquetadas
        self.acum_botadas += acum_botadas
        self.acum_destruidas += acum_destruidas
        self.acum_empaquetadas += acum_empaquetadas
        self.acum_servicio += acum_servicio
        self.clock += clock
        self.section1QueueSize += len(section1Queue)
        self.section2QueueSize += len(section2Queue)
        self.llegadas += llegadas
        self.employee1Time += employee1Time
        self.employee2Time += employee2Time
        self.employee3Time += employee3Time

    def start(self):
        for i in range(self.repetitions):
            sim = Simulation(i, self.maxTime, self.distributions[0], self.distributions[1], self.distributions[2], self.distributions[3])
            sim.run()
            self.get_sim_stats(sim)
            sim.print_statistics()

        self.print_statistics()

    def start_test(self):
        # Llena las distribuciones por defecto en vez de pedir al usuario que las digite
        self.distributions.append(Uniform(3, 6))
        self.distributions.append(Uniform(1, 3))
        self.distributions.append(Uniform(1, 3))
        self.distributions.append(Uniform(1, 3))

        # Ahora que se tienen los parámetros, llama a start para que se encargue de la simulación
        self.start()
        
        
    def print_statistics(self):
        masks_lost = self.botadas + self.destruidas 
        total_masks = masks_lost + self.empaquetadas 
        lost_masks_time = self.acum_botadas + self.acum_destruidas
        total_mask_time = lost_masks_time + self.acum_empaquetadas
        mean_service_time = self.acum_servicio / total_masks

        print("\n\n------------ESTADÍSTICAS FINALES DE LA SIMULACIÓN------------\n")
        print("Tiempo promedio que corrieron las simulaciones: " + str(round(self.clock/self.repetitions,2)) + " minutos"  )
        print("Longitud promedio de la cola en sección 1: " + str(self.section1QueueSize/self.repetitions) )
        print("Longitud promedio de la cola en sección 2: " + str(self.section2QueueSize/self.repetitions) )
        print("Tiempo promedio que pasa una mascarilla en el sistema antes de botarse o destruirse: " + str( round(lost_masks_time/masks_lost, 2) ) + " minutos")
        print("Tiempo promedio que pasa una mascarilla en el sistema antes de empaquetarse: " + str( round(self.acum_empaquetadas/self.empaquetadas,2) )+ " minutos")
        print("Tiempo promedio que pasa una mascarilla en el sistema en general: " + str(round(total_mask_time/total_masks, 2))+ " minutos")
        print("Tiempo promedio de servicio para una mascarilla en el sistema en general: " + str(round(mean_service_time,2)) + " minutos")
        print("Eficiencia promedio del sistema (Ws/W): " + str(round(mean_service_time / total_mask_time * total_masks, 2)))
        print("Equilibrio promedio del sistema: " + str( round(self.llegadas / total_masks, 2) ) )
        print("Promedio de máscaras que llegaron: " + str(round(total_masks/self.repetitions, 2)) )
        print("\tPromedio de máscaras que se botaron (o destruyeron): " + str(round(masks_lost/self.repetitions,2)) + " (" + str(round(masks_lost/total_masks * 100, 2)) + "%)")
        print("\tPromedio de máscaras que se empacaron: " + str(round(self.empaquetadas/self.repetitions,2)) + " (" + str(round(self.empaquetadas/total_masks * 100, 2)) + "%)")
        print("Porcentaje promedio de tiempo real de trabajo de los empleados:")
        print("\tTrabajo real promedio del empleado de sección 1: " + str(round(self.employee1Time / self.clock, 2)) )
        print("\tTrabajo real promedio del empleado 1 de sección 2: " + str(round(self.employee2Time / self.clock, 2)) )
        print("\tTrabajo real promedio del empleado 2 de sección 2: " + str(round(self.employee3Time / self.clock, 2)) )
