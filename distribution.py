import math
import random
import numpy as np

"""
    Clase padre para los cinco tipos de distribuciones que se manejan.
"""
class Distribution:
    def generate_random_value(self):
        return 0

    def read_distribution(self):
        print("")

"""
    Clase para la distribución uniforme.
    En esta distribución se generan valores entre un a y un b, todos con el mismo chance de generarse.
"""
class Uniform(Distribution):
    def __init__(self, a = 0.0, b = 0.0):
        self.a = a
        self.b = b

    # Genera un valor aleatorio entre a y b.
    def generate_random_value(self):
        # Se genera un número aleatorio entre 0 y 1
        r = random.random()

        # Se calcula x = r * (b-a+1) + a
        return (r * (self.b -self.a)) + self.a

    # Método para leer el a y b de la entrada estándar, en caso de que no se haya definido al crear el objeto Uniform.
    def read_distribution(self):
        while True:
            self.a = float(input('\tPor favor digite el valor para a: '))
            self.b = float(input('\tPor favor digite el valor para b: '))

            if (self.a < self.b): 
                break
            else:
                print("\tError, a debe ser un número menor que b\n")

    # Método para cambiar los parámetros de a y b, en caso de que se ocupe cambiar o no se haya definido al principio.
    def set_parameters(self, a, b):
        self.a = a 
        self.b = b

"""
    Clase para la generación de valores aleatorios con distribución normal por método directo.
"""
class DirectNormal(Distribution):
    def __init__(self, mean = 0.0, variance = 0.0):
        self.mean = mean
        self.variance = variance

    # Método que genera un valor aleatorio, a partir de otro valor aleatorio z. Este valor z sale usando coordenadas polares para encontrar su valor.
    def generate_random_value(self):
        # Se generan dos números aleatorios entre 0 y 1
        r_1 = random.random()
        r_2 = random.random()

        # En este caso decidimos utilizar solo la fórmula para z1, con el coseno
        z = math.sqrt(-2 * np.log(r_1)) * math.cos(2 * math.pi * r_2) 

        # Aquí es con la fórmula de  x = sigma * z + mu
        return self.variance * z + self.mean

    # Método para leer el mean y variance de la entrada estándar, en caso de que no se haya definido al crear el objeto DirectNormal.
    def read_distribution(self):
        self.mean = float(input('\tPor favor digite el valor para la media: '))
        self.variance = float(input('\tPor favor digite el valor para la varianza: '))

"""
    Clase para la generación de valores aleatorios con distribución normal por método de la convolución.
"""
class ConvolutionNormal(Distribution):
    def __init__(self, mean = 0.0, variance = 0.0):
        self.mean = mean
        self.variance = variance
    
    # Método que genera un valor aleatorio, a partir de otro valor aleatorio z. 
    # Este valor z sale sacando otros 12 valores aleatorios entre 0 y 1, sumándolos entre sí y a ese resultado restarle 6.
    def generate_random_value(self):
        z = 0

        # Esto es siguiendo la fórmula simplicada que se da en el libro
        # donde se toma que K = 12, por lo que al final solo tenemos que 
        # z = sum de 0 a 12 de r_i
        for _ in range(12):
            z += random.random()
        # A la suma después se le resta 6
        z -= 6

        # Aquí es con la fórmula de  x = sigma * z + mu
        return self.variance * z + self.mean
    
    # Método para leer el mean y variance de la entrada estándar, en caso de que no se haya definido al crear el objeto ConvolutionNormal.
    def read_distribution(self):
        self.mean = float(input('\tPor favor digite el valor para la media: ') )
        self.variance = float(input('\tPor favor digite el valor para la varianza: ') )

"""
    Clase para la generación de valores aleatorios con distribución exponencial.
    Se obtienen valores por el método de transformación inversa con la distribución acumulativa de la exponencial.
"""
class Exponential(Distribution):
    def __init__(self, lambd = 0.0):
        self.lambd = lambd

    # Método que genera un valor aleatorio usando transformación inversa sobre la función de distribución acumulativa de la exponencial.
    def generate_random_value(self):
        # Generamos un valor aleatorio entre 0 y 1
        r = random.random()

        # Esto es utilizando la fórmula vista en clases para la
        # distribución exponencial con el ITM: x = -ln(r)/lambda
        return -1 * (np.log(r)/self.lambd)

    # Método para leer el lambda si no se pudo definir al crear el objeto Exponential.
    def read_distribution(self):
        self.lambd = float(input('\tPor favor digite el valor para lambda: '))

"""
    Clase para la generación de valores aleatorios con distribución dada por la función f(x)=kx.
    Se obtienen valores por el método de transformación inversa con la distribución acumulativa de la función f(x)=kx, es decir, F(x)=kx^2/2.
"""
class DensityFunction(Distribution):
    def __init__(self, a = 0.0, b = 0.0, k = 0.0):
        self.a = a
        self.b = b
        self.k = k

        # Para que r solo esté en el rango [F(a), F(b)], es decir, [k*a^2/2, k*b^2/2]
        self.uniform = Uniform(self.k * self.a * self.a / 2, self.k * self.b * self.b / 2)

    # Genera un valor aleatorio usando el método de transformación inversa con F(x)=kx^2/2.
    def generate_random_value(self):
        # Se obtiene un r entre [F(a), F(b)]
        r = self.uniform.generate_random_value()

        # Esto es después de haber obtenido la integral de f(x) = kx con ITM
        # Al final se obtuvo que x = sqrt(2r / k)
        return math.sqrt( 2 * r / self.k )

    # Método para leer el a, b y k de la entrada estándar, en caso de que no se haya definido al crear el objeto DensityFunction.
    def read_distribution(self):
        while True:
            self.a = float(input('\tPor favor digite el valor para a: '))
            self.b = float(input('\tPor favor digite el valor para b: '))
            self.k = float(input('\tPor favor digite el valor para k: '))
            self.uniform.set_parameters(self.k * self.a * self.a / 2, self.k * self.b * self.b / 2)

            if (self.a < self.b): 
                break
            else:
                print("Error, a debe ser un número menor que b")
