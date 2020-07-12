"""
    Clase para las máscaras del sistema.
    En esta clase se lleva cuenta de cuándo entró al sistema la máscara y de su tiempo total que pasa siendo atendida por un encargado.
"""
class Mask:
    def __init__(self, init_time):
        self.init_time = init_time
        self.init_service_time = 0
        self.cumulative_service_time = 0

    # Método que se llama cuando la máscara va a ser atendida por un encargado.
    def start_service_time(self, time):
        self.init_service_time = time

    # Método que se llama cuando la máscara termina de ser atendida por el encargado. Aquí se acumula el tiempo de servicio.
    def end_service_time(self, end_time):
        self.cumulative_service_time += (end_time - self.init_service_time)
        self.init_service_time = 0