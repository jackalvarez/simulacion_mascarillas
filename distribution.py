class Distribution:
    def generate_random_value(self):
        print("si, pa?")
        return 0

class Uniform(Distribution):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def generate_random_value(self):
        print("algun dia :v")
        return 0

class DirectNormal(Distribution):
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance
    def generate_random_value(self):
        print("algun dia :v")
        return 0

class ConvolutionNormal(Distribution):
    def __init__(self, mean, variance):
        self.mean = mean
        self.variance = variance
    def generate_random_value(self):
        print("algun dia :v")
        return 0

class Exponential(Distribution):
    def __init__(self, lambd):
        self.lambd = lambd
    def generate_random_value(self):
        print("algun dia :v")
        return 0

class DensityFunction(Distribution):
    def __init__(self, a, b, k):
        self.a = a
        self.b = b
        self.k = k
    def generate_random_value(self):
        print("algun dia :v")
        return 0