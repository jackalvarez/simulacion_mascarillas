from mask import Mask

"""
    Clase padre para los dos tipos de encargados que existen en el sistema, el de la sección 1 y los de la sección 2.
    Aquí se tiene la parte que tienen en común los encargados, que tienen que ir acumulando su tiempo de servicio, 
    para obtener el tiempo que pasan trabajando
"""
class Employee:

    def __init__(self, warm_up_time):
        self.disponible = True
        self.init_time = 0
        self.acum_service_time = 0
        self.warm_up_time = warm_up_time

    # Método donde se marca cuando inició a atender a las mascarillas.
    def start_service(self, init_time):
        self.init_time = init_time
        self.disponible = False

    # Método donde se termina de atender a las mascarillas y se aumenta en el acumulado de tiempos de servicio.
    def end_service(self, end_time):
        if self.init_time > self.warm_up_time:
            self.acum_service_time += (end_time - self.init_time)
        self.init_time = 0
        self.disponible = True

"""
    Clase para el empleado de la sección 1, que solo tiene de cliente a una única máscara.
"""
class EmployeeSection1(Employee):
    def __init__(self, warm_up_time):
        super().__init__(warm_up_time)
        self.mask = None

    # Método que se llama al empezar a atender a una máscara. Aquí se inicia el tiempo de servicio para la máscara y el encargado.
    def set_current_mask(self, init_time, mask):
        self.mask = mask
        self.mask.start_service_time(init_time)
        super().start_service(init_time)

    # Método que se llama cuando el servicio termina. Se llama a terminar el tiempo de servicio de la máscara y del encargado, para aumentar los acumuladores.
    def service_ends(self, end_time):
        self.mask.end_service_time(end_time)
        self.mask = None
        super().end_service(end_time)

"""
    Clase para los empleados de la sección 2, que tienen de cliente parejas de máscaras.
"""
class EmployeeSection2(Employee):
    def __init__(self, warm_up_time):
        super().__init__(warm_up_time)
        self.mask1 = None
        self.mask2 = None

    # Método que se llama al empezar a atender dos máscaras. Aquí se inicia el tiempo de servicio para las máscaras y el encargado.
    def set_current_masks(self, init_time, mask1, mask2):
        self.mask1 = mask1
        self.mask2 = mask2
        super().start_service(init_time)

        self.mask1.start_service_time(init_time)
        self.mask2.start_service_time(init_time)

    # Método que se llama cuando el servicio termina. Se llama a terminar el tiempo de servicio de las máscaras y del encargado, para aumentar los acumuladores.
    def service_ends(self, end_time):
        self.mask1.end_service_time(end_time)
        self.mask2.end_service_time(end_time)
        self.mask1 = None
        self.mask2 = None
        super().end_service(end_time)