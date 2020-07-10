from simulation_manager import SimulationManager

import sys
from sys import argv
from sys import exit

if __name__=="__main__":

    print("Inicio del proyecto Simulación de Mascarillas")
    print("Para el curso de Modelado y Optimización\n")

    # Si no se digita ningún parámetro al llamar al programa, entonces
    # se piden al usuario los valores para las repeticiones y el tiempo 
    # máximo que puede correr cada simulación
    if len(sys.argv) != 3:
        repetitions = int(input('Número de corridas: '))
        maxTime = float(input('Tiempo máximo a correr: '))

        # Llama al método constructor de la simulación. 
        sim = SimulationManager(repetitions, maxTime)

        # Método donde se le pide al usuario que elija las 4 distribuciones
        sim.read_distributions()

        # Método que inicia el proyecto con todas las simulaciones
        sim.start()

     # En caso de que sí se ingresen parámetros al correr el programa
    elif(sys.argv[1] == '--test'):
        sim = SimulationManager()
        sim.start_test(int(sys.argv[2]) )