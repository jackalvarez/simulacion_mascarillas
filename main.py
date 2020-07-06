from simulation import Simulation

from sys import argv
from sys import exit

if __name__=="__main__":
    
    repetitions = input('Número de corridas: ')
    maxTime = float(input('Tiempo máximo a correr: '))


    sim = Simulation(maxTime)
    sim.run()