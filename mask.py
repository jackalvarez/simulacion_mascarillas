class Mask:
    def __init__(self, init_time):
        self.init_time = init_time
        self.init_service_time = 0
        self.cumulative_service_time = 0
    def start_service_time(self, time):
        self.init_service_time = time
    def end_service_time(self, end_time):
        self.cumulative_service_time += (end_time - self.init_service_time)
        self.init_service_time = 0