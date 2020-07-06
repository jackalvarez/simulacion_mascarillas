from mask import Mask

class Employee:
    def __init__(self):
        self.cumulative_time = 0
        self.service_count = 0

        self.init_current_time = 0

        self.disponible = True
    def service_begins(self, init_time):
        self.init_current_time = init_time
        self.disponible = False
    def service_ends(self, end_time):
        self.cumulative_time += (end_time - self.init_current_time)
        self.service_count += 1
        self.init_current_time = 0
        self.disponible = True

class EmployeeSection1(Employee):
    def __init__(self):
        self.mask = None
    def set_current_mask(self, init_time, mask):
        self.mask = mask
        super().service_begins(init_time)
    def service_ends(self, end_time):
        self.mask = None
        super().service_ends(end_time)

class EmployeeSection2(Employee):
    def __init__(self):
        self.mask1 = None
        self.mask2 = None
    def set_current_masks(self, init_time, mask1, mask2):
        self.mask1 = mask1
        self.mask2 = mask2
        super().service_begins(init_time)
    def service_ends(self, end_time):
        self.mask1 = None
        self.mask2 = None
        super().service_ends(end_time)