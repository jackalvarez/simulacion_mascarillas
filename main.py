from simulation_manager import SimulationManager

import sys
from sys import argv
from sys import exit

if __name__=="__main__":

    print("Inicio del proyecto Simulación de Mascarillas")
    print("Para el curso de Modelado y Optimización\n")
    if len(sys.argv) != 2:
        repetitions = int(input('Número de corridas: '))
        maxTime = float(input('Tiempo máximo a correr: '))

        sim = SimulationManager(repetitions, maxTime)
        sim.read_distributions()
        sim.start()
    elif(sys.argv[1] == '--test'): # En caso de que se estén haciendo pruebas, llena los parámetros por defecto
        repetitions = 10
        maxTime = 5000

        sim = SimulationManager(repetitions, maxTime)
        sim.start_test()