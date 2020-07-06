import math
import random
import numpy as np

class Distribution:
    def generate_random_value(self):
        print("si, pa?")
        return 0

class Uniform(Distribution):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def generate_random_value(self):
        r = random.random()
        return (r % (self.b -self.a + 1)) + self.a

class DirectNormal(Distribution):
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance
    def generate_random_value(self):
        r_1 = random.random()
        r_2 = random.random()
        z = math.sqrt(-2 * np.log(r_1)) * math.cos(2 * math.pi * r_2) 
        return self.variance * z + self.mean

class ConvolutionNormal(Distribution):
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance
    def generate_random_value(self):
        z = 0
        for i in range(12):
            z += random.random() - 6

        return self.variance * z + self.mean

class Exponential(Distribution):
    def __init__(self, lambd):
        self.lambd = lambd
    def generate_random_value(self):
        r = random.random()
        return -1 * (np.log(r)/self.lambd)

class DensityFunction(Distribution):
    def __init__(self, a, b, k):
        self.a = a
        self.b = b
        self.k = k
    def generate_random_value(self):
        # Para que r solo esté en el rango [k*a, k*b]
        r = random.randint(self.k*self.a, self.k*self.b)

        return math.sqrt( 2 * r / self.k )