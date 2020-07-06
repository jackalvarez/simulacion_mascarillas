class SimulationManager:
    def __init__(self, repetitions, maxTime):
        self.repetitions = repetitions
        self.maxTime = maxTime

        self.totalRunTime = 0
        
        self.colaEsperaDesinfeccion = []
        self.colaEsperaEmpaquetado = []
        
        
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


        
        