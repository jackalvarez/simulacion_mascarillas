from simulation_manager import SimulationManager

from sys import argv
from sys import exit

if __name__=="__main__":
    
    repetitions = int(input('Número de corridas: '))
    maxTime = float(input('Tiempo máximo a correr: '))

    sim = SimulationManager(repetitions, maxTime)
    sim.read_distributions()
    sim.start()