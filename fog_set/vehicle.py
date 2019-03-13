class Vehicle:
    used_bit        = False
    max_traffic     = 0
    real_usage_time = 0
    def __init__(self, index, cost, consumption_rate, initial_power, threshold_power):
        self.index              = index
        self.cost               = cost
        self.consumption_rate   = consumption_rate
        self.initial_power      = initial_power
        self.threshold_power    = threshold_power
        self.usage_time         = (self.initial_power - self.threshold_power)/self.consumption_rate
    
    def used(self, max_latency):
        if self.usage_time >= max_latency:
            self.real_usage_time = max_latency
            return True
        else:
            return False