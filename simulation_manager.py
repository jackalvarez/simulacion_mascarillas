from distribution import Distribution, Uniform, DirectNormal, ConvolutionNormal, Exponential, DensityFunction
from simulation import Simulation

import math
import string

class SimulationManager:
    def __init__(self, repetitions = 10, maxTime = 5000):
        # Las cantidad de simulaciones a realizar. Por defecto es 10
        self.repetitions = repetitions

        # El máximo tiempo que va a correr cada simulación. Por defecto es 500
        self.maxTime = maxTime
        
        # Distribuciones
        self.distributions = []

        # Datos para las estadísticas
        self.clock = 0
        self.section1QueueSize = 0
        self.section2QueueSize = 0

        self.totalRunTime = 0
        
        self.totalQueueSizeSection1 = 0
        self.totalQueueSizeSection2 = 0

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

        # Para el tiempo que pasa una mascarilla en el sistema en general
        self.times = []
        self.mean_time = 0

        # Para saber cuál es la simulación en la que estoy
        self.current_sim = 0

    # Este método crea las instancias de las distintas distribuciones. Recibe
    # la opción que digitó el usuario y devuelve una distribución del tipo de
    # distribución acorde  
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

        # Se imprimen las opciones de las distribuciones
        print('Considere las siguientes distribuciones:')
        print('\ta) distribución uniforme en (a,b)')
        print('\tb) distribución normal - método directo')
        print('\tc) distribución normal - método de la convolución')
        print('\td) distribución exponencial parámetro lambda')
        print('\te) distribución con función de densidad: f(x) = kx')
        
        # Se pide y registra la distribución deseada para cada una de las 4 distribuciones
        for i in range(4):
            choice = input('\n\tPor favor digite la letra [a-e] de la distribución que desea para D' + str(i + 1) + ': ')
                
            # Se va a pedir que seleccione la distribución hasta que digite una opción válida
            while choice not in  list(string.ascii_lowercase[0:5]):
                print("\tError. La opción debe ser una letra entre a y e.")
                choice = input('\n\tPor favor digite la letra [a-e] de la distribución que desea para D' + str(i + 1) + ': ')

            # Se agrega la distribución actual a la lista de distribuciones
            self.distributions.append( self.distribution_factory(choice))

            # Se llama al método que sabe pedir los parámetros que ocupa la distribución elegida
            self.distributions[i].read_distribution()
    
    # Este método es el que toma los datos de cada una de las simulaciones, cada vez que estas terminan de ejecutar
    # Toma los datos que devuelven las demás simulaciones, y se los suma a los contadores actuales
    def get_sim_stats(self, sim):
        # Se llama al método getStatistics(), que devuelve todos los valores de la simulación
        botadas, destruidas, empaquetadas, acum_botadas, acum_destruidas, acum_empaquetadas, acum_servicio, clock, section1Queue, section2Queue, llegadas, employee1Time, employee2Time, employee3Time, mean_time = sim.getStatistics()
        
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
        self.mean_time += mean_time

        # Se asigna el tiempo promedio de cada simulación, porque para el intervalo de confianza ocupamos cada uno de los tiempos
        self.times.append(mean_time)

    # Este es el método para iniciar todo el proyecto. Se encarga de que se hagan todas las simulaciones, obtiene las estadísticas,
    # y llama a los métodos necesarios para que impriman las estadísticas finales.
    def start(self):
        for i in range(self.repetitions):
            self.current_sim = i
            sim = Simulation(i, self.maxTime, self.distributions[0], self.distributions[1], self.distributions[2], self.distributions[3])
            sim.run()
            self.get_sim_stats(sim)
            sim.print_statistics()
            input("\nDigite cualquier tecla para continuar con la siguiente simulación: ")

        self.print_statistics()

    # Este método llena las distribuciones por defecto en vez de pedir al usuario 
    # que las digite. Si recibe el parámetro 1, llena con las distribuciones que
    # se enviaron por correo, con las exponenciales con lambda = 1,3,2,2. Si se 
    # recibe el modo 2, se corren con las otras distribuciones no exponenciales
    def start_test(self, mode):
        # Revisa cuál es el modo con el que se tiene que correr el programa

        while( mode != 1 and mode != 2):
            print("Error, modo de prueba incorrecto")
            mode = int(input("Por favor digite el número de distribuciones a probar (exponenciales = 1, normales = 2): "))

        if (mode == 1):
            self.distributions.append(Exponential(1))
            self.distributions.append(Exponential(3))
            self.distributions.append(Exponential(2))
            self.distributions.append(Exponential(2))
        elif (mode == 2):
            self.distributions.append(DirectNormal(1.3,0.01))
            self.distributions.append(Uniform(0.21, 0.9))
            self.distributions.append(DensityFunction(3, 6, 2.0/27.0))
            self.distributions.append(ConvolutionNormal(4.0/3.0, 0.0001))    

        # Ahora que se tienen los parámetros, llama a start para que se encargue de la simulación
        self.start()
        
        
    def print_statistics(self):
        # Cálculos para las estadísticas
        masks_lost = self.botadas + self.destruidas 
        total_masks = masks_lost + self.empaquetadas 
        lost_masks_time = self.acum_botadas + self.acum_destruidas
        total_mask_time = lost_masks_time + self.acum_empaquetadas
        mean_service_time = self.acum_servicio / total_masks

        # Se imprimen todas las estadísticas con los números redondeados a 2 decimales
        print("\n\n------------ESTADÍSTICAS FINALES DE LA SIMULACIÓN------------\n")
        print("Tiempo promedio que corrieron las simulaciones: " + str(round(self.clock/self.repetitions,2)) + " minutos"  )
        print("Longitud promedio de la cola en sección 1: " + str(self.section1QueueSize/self.repetitions) )
        print("Longitud promedio de la cola en sección 2: " + str(self.section2QueueSize/self.repetitions) )
        print("Tiempo promedio que pasa una mascarilla en el sistema antes de botarse o destruirse: " + str( round(lost_masks_time/masks_lost, 2) ) + " minutos")
        print("Tiempo promedio que pasa una mascarilla en el sistema antes de empaquetarse: " + str( round(self.acum_empaquetadas/self.empaquetadas,2) )+ " minutos")
        print("Tiempo promedio de servicio para una mascarilla en el sistema: " + str(round(mean_service_time,2)) + " minutos")
        print("Eficiencia promedio del sistema (Ws/W): " + str(round(mean_service_time / total_mask_time * total_masks, 2)))
        print("Equilibrio promedio del sistema: " + str( round(self.llegadas / total_masks, 2) ) )
        print("Promedio de máscaras que llegaron: " + str(round(self.llegadas/self.repetitions, 2)) )
        print("\tPromedio de máscaras que se botaron (o destruyeron): " + str(round(masks_lost/self.repetitions,2)) + " (" + str(round(masks_lost/self.llegadas * 100, 2)) + "%)")
        print("\tPromedio de máscaras que se empacaron: " + str(round(self.empaquetadas/self.repetitions,2)) + " (" + str(round(self.empaquetadas/self.llegadas * 100, 2)) + "%)")
        print("Porcentaje promedio de tiempo real de trabajo de los empleados:")
        print("\tTrabajo real promedio del empleado de sección 1: " + str(round(self.employee1Time / self.clock, 2)) )
        print("\tTrabajo real promedio del empleado 1 de sección 2: " + str(round(self.employee2Time / self.clock, 2)) )
        print("\tTrabajo real promedio del empleado 2 de sección 2: " + str(round(self.employee3Time / self.clock, 2)) )

        # Se calculan los valores para el intervalo de confianza
        media_muestral = self.mean_time/self.repetitions
        
        print("Tiempo promedio que pasa una mascarilla en el sistema en general: " + str(round(media_muestral, 2))+ " minutos")

        # Cuando solo hay 10 repeticiones, se calcula e imprime el intervalo de confianza
        if (self.repetitions == 10):
            varianza_muestral = 0

            # Se hace la sumatoria de las diferencias con la media para calcular la varianza
            for i in range(self.repetitions):
                varianza_muestral += pow((self.times[i] - media_muestral),2)/(self.repetitions-1)
                #print('El tiempo fue de: ' + str(self.times[i]))
                #print('La varianza es de: ' + str(varianza_muestral))

            # Este es el valor que se va a sumar y restar para obtener los límites superiores e inferiores
            rango = 2.26 * math.sqrt(abs(varianza_muestral)/10)

            lim_inferior = media_muestral - rango
            lim_superior = media_muestral + rango

            #print('\nla media es de: ' + str(media_muestral))
            #print('la varianza es de: '  +str(varianza_muestral))
            print("Con un intervalo de confianza de [" + str(round(lim_inferior,4)) + ", " + str(round(lim_superior,4)) + "]")
        