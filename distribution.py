import math
import random
import numpy as np

class Distribution:
    def generate_random_value(self):
        return 0

    def read_distribution(self):
        print("")

class Uniform(Distribution):
    def __init__(self, a = 0, b = 0):
        self.a = a
        self.b = b
    def generate_random_value(self):
        # Se genera un número aleatorio entre 0 y 1
        r = random.random()

        # Se calcula x = r * (b-a+1) + a
        return (r * (self.b -self.a)) + self.a

    def read_distribution(self):
        self.a = float(input('\tPor favor digite el valor para a: '))
        self.b = float(input('\tPor favor digite el valor para b: '))

    def set_parameters(self, a, b):
        self.a = a 
        self.b = b


class DirectNormal(Distribution):
    def __init__(self, mean = 0, variance = 0):
        self.mean = mean
        self.variance = variance
    def generate_random_value(self):
        # Se generan dos números aleatorios entre 0 y 1
        r_1 = random.random()
        r_2 = random.random()

        # En este caso decidimos utilizar solo la fórmula para z1, con el coseno
        z = math.sqrt(-2 * np.log(r_1)) * math.cos(2 * math.pi * r_2) 

        # Aquí es con la fórmula de  x = sigma * z + mu
        return self.variance * z + self.mean

    def read_distribution(self):
        self.mean = float(input('\tPor favor digite el valor para la media: '))
        self.variance = float(input('\tPor favor digite el valor para la varianza: '))

class ConvolutionNormal(Distribution):
    def __init__(self, mean = 0, variance = 0):
        self.mean = mean
        self.variance = variance
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
    
    def read_distribution(self):
        self.mean = float(input('\tPor favor digite el valor para la media: ') )
        self.variance = float(input('\tPor favor digite el valor para la varianza: ') )

class Exponential(Distribution):
    def __init__(self, lambd = 0):
        self.lambd = lambd
    def generate_random_value(self):
        # Generamos un valor aleatorio entre 0 y 1
        r = random.random()

        # Esto es utilizando la fórmula vista en clases para la
        # distribución exponencial con el ITM: x = -ln(r)/lambda
        return -1 * (np.log(r)/self.lambd)

    def read_distribution(self):
        self.mean = float(input('\tPor favor digite el valor para lambda: '))

class DensityFunction(Distribution):
    def __init__(self, a = 0, b = 0, k = 0):
        self.a = a
        self.b = b
        self.k = k

        # Para que r solo esté en el rango [F(a), F(b)], es decir, [k*a^2/2, k*b^2/2]
        self.uniform = Uniform(self.k * self.a * self.a / 2, self.k * self.b * self.b / 2)

    def generate_random_value(self):
        # Se obtiene un r entre [F(a), F(b)]
        r = self.uniform.generate_random_value()

        # Esto es después de haber obtenido la integral de f(x) = kx con ITM
        # Al final se obtuvo que x = sqrt(2r / k)
        return math.sqrt( 2 * r / self.k )

    def read_distribution(self):
        self.a = float(input('\tPor favor digite el valor para a: '))
        self.b = float(input('\tPor favor digite el valor para b: '))
        self.k = int(input('\tPor favor digite el valor para k: '))