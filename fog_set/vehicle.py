class Vehicle:
    used_bit    = False
    def __init__(self, index, cost, consumption_rate, initial_power, threshold_power):
        self.index              = index
        self.cost               = cost
        self.consumption_rate   = consumption_rate
        self.initial_power      = initial_power
        self.threshold_power    = threshold_power
        self.usage_time         = (self.initial_power - self.threshold_power)/self.consumption_rate
    
    def used(self, max_latency):
        if self.usage_time >= max_latency:
            return True
        else:
            return False