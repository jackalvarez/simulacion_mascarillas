import math
import random
import numpy as np

class Distribution:
    def generate_random_value(self):
        return 0

class Uniform(Distribution):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def generate_random_value(self):
        # Se genera un número aleatorio entre 0 y 1
        r = random.random()

        # Se calcula x = r * (b-a+1) + a
        return (r * (self.b -self.a)) + self.a

class DirectNormal(Distribution):
    def __init__(self, mean, variance):
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

class ConvolutionNormal(Distribution):
    def __init__(self, mean, variance):
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

class Exponential(Distribution):
    def __init__(self, lambd):
        self.lambd = lambd
    def generate_random_value(self):
        # Generamos un valor aleatorio entre 0 y 1
        r = random.random()

        # Esto es utilizando la fórmula vista en clases para la
        # distribución exponencial con el ITM: x = -ln(r)/lambda
        return -1 * (np.log(r)/self.lambd)

class DensityFunction(Distribution):
    def __init__(self, a, b, k):
        self.a = a
        self.b = b
        self.k = k

        # Para que r solo esté en el rango [f(a), f(b)], es decir, [k*a, k*b]
        self.uniform = Uniform(self.k * self.a, self.k * self.b)

    def generate_random_value(self):
        # Se obtiene un r entre [f(a), f(b)]
        r = self.uniform.generate_random_value()

        # Esto es después de haber obtenido la integral de f(x) = kx con ITM
        # Al final se obtuvo que x = sqrt(2r / k)
        return math.sqrt( 2 * r / self.k )