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
        
    def start(self):
        for i in range(self.repetitions):
            print("Inicia la simulación " + str(i + 1)) 
            sim = Simulation(i, self.maxTime, self.distributions[0], self.distributions[1], self.distributions[2], self.distributions[3])
            sim.run()
            sim.print_statistics()

    def start_test(self):
        # Llena las distribuciones por defecto en vez de pedir al usuario que las digite
        self.distributions.append(Uniform(10, 15))
        self.distributions.append(Uniform(10, 15))
        self.distributions.append(Uniform(10, 15))
        self.distributions.append(Uniform(10, 15))

        # Ahora que se tienen los parámetros, llama a start para que se encargue de la simulación
        self.start()
        
        
    def print_statistics(self):
        print("\n\n------------ESTADÍSTICAS FINALES DE LA SIMULACIÓN------------\n")
        print("Tiempo promedio que corrieron las simulaciones: " + self.totalRunTime/self.repetitions + "minutos" )
        print("Longitud promedio de la cola en sección 1: " + self.totalQueueSizeSection1 / self.repetitions)
        print("Longitud promedio de la cola en sección 2: " + self.totalQueueSizeSection2 / self.repetitions)
        
