from mask import Mask

class Employee:
    def __init__(self):
        self.disponible = True
        self.init_time = 0
        self.acum_service_time = 0
    def start_service(self, init_time):
        self.init_time = init_time
        self.disponible = False
    def end_service(self, end_time):
        self.acum_service_time += (end_time - self.init_time)
        self.init_time = 0
        self.disponible = True

class EmployeeSection1(Employee):
    def __init__(self):
        super().__init__()
        self.mask = None
    def set_current_mask(self, init_time, mask):
        self.mask = mask
        self.mask.start_service_time(init_time)
        super().start_service(init_time)

    def service_ends(self, end_time):
        self.mask.end_service_time(end_time)
        self.mask = None
        super().end_service(end_time)

class EmployeeSection2(Employee):
    def __init__(self):
        super().__init__()
        self.mask1 = None
        self.mask2 = None
    def set_current_masks(self, init_time, mask1, mask2):
        self.mask1 = mask1
        self.mask2 = mask2
        super().start_service(init_time)

        self.mask1.start_service_time(init_time)
        self.mask2.start_service_time(init_time)

    def service_ends(self, end_time):
        self.mask1.end_service_time(end_time)
        self.mask2.end_service_time(end_time)
        self.mask1 = None
        self.mask2 = None
        super().end_service(end_time)