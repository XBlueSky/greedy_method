from m_m_c.m_m_c import m_m_c_latency
from fog_set.vehicle import Vehicle

class Fog:
    used            = False
    vehicle_set     = []
    used_vehicles   = 0
    max_traffic     = 0
    latency         = 0

    def __init__(self, index, capacity, total_vehicles, edge_transmission_rate, fog_transmission_rate):
        self.index                      = index
        self.capacity                   = capacity
        self.total_vehicles             = total_vehicles
        self.edge_transmission_rate     = edge_transmission_rate
        self.fog_transmission_rate      = fog_transmission_rate
    
    def set_vehicle_set(self, cost_set = [], consumption_rate_set = [], initial_power_set = [], threshold_power_set = []):
        self.vehicle_set = []
        for i in range(self.total_vehicles):
            self.vehicle_set.append( Vehicle( i, cost_set[i], consumption_rate_set[i], initial_power_set[i], threshold_power_set[i]))

    def computation_latency(self, traffic, used_vehicles):
        return m_m_c_latency(used_vehicles, traffic, self.capacity)

    def edge_communication_latency(self, traffic):
        return m_m_c_latency(1, traffic, self.edge_transmission_rate)
    
    def fog_communication_latency(self, traffic):
        return m_m_c_latency(1, traffic, self.fog_transmission_rate)

    def used_bits_list(self):
        return [v.used_bit for v in sorted(self.vehicle_set, key=lambda v : v.index)]
    
    def fog_cost(self):
        return sum([v.used_bit * v.cost for v in self.vehicle_set])
    
    def fog_fixed_cost(self, cost):
        return sum([v.used_bit * cost for v in self.vehicle_set])
    
    def clear(self):
        self.max_traffic    = 0
        self.used_vehicles  = 0
        self.latency        = 0
        self.used           = False
        for f in self.vehicle_set:
            f.used_bit = False

    # offloading computation from edge to fog
    def algorithm(self, traffic, max_latency, least_error):
        
        # start from number of vehicles whose usage_time bigger equal than max_latency
        self.vehicle_set.sort(key=lambda v : v.cost)
        self.vehicle_set.sort(key=lambda v : v.usage_time, reverse=True)
        used_vehicles = sum([v.used(max_latency) for v in self.vehicle_set])

        # find maximum traffic
        # check arrival traffic is larger than the traffic that can be handle in edge
        total_latency = self.edge_communication_latency(traffic) + self.computation_latency(traffic, used_vehicles) + self.fog_communication_latency(traffic)

        if total_latency > max_latency:

            # find least traffic by bisection method variation
            self.max_traffic = self.bisection_method(traffic, used_vehicles, max_latency, least_error)

            # find maximum traffic from least traffic plus one by one
            for vehicles_num in range(used_vehicles + 1, self.total_vehicles + 1):

                test_traffic = self.bisection_method(traffic, vehicles_num, self.vehicle_set[vehicles_num - 1].usage_time, least_error)
                if test_traffic > self.max_traffic:
                    self.max_traffic = test_traffic
                    used_vehicles = vehicles_num
                else:
                    break
        
        else:
            self.max_traffic = traffic

            # find minmum number of used vehicles to handle the traffic
            # linear search
            communication_latency = self.edge_communication_latency(traffic) + self.fog_communication_latency(traffic)
                
            while self.computation_latency(self.max_traffic, used_vehicles) <= max_latency - communication_latency:
                used_vehicles = used_vehicles - 1 
            used_vehicles = used_vehicles + 1
        
        for num in range(used_vehicles):
            self.vehicle_set[num].used_bit = True
        self.used_vehicles = used_vehicles
        communication_latency = self.edge_communication_latency(self.max_traffic) + self.fog_communication_latency(self.max_traffic)
        self.latency = communication_latency + self.computation_latency(self.max_traffic, self.used_vehicles)

    def bisection_method(self, traffic, used_vehicles, max_latency, least_error):
        lower   = 0
        upper   = traffic
        flag    = False

        while (lower + least_error) <= upper:
            mid = (lower + upper) / 2
            total_latency = self.edge_communication_latency(mid) + self.computation_latency(mid, used_vehicles) + self.fog_communication_latency(mid)

            if total_latency <= max_latency:
                flag    = True
                lower   = mid
            else:
                upper   = mid

        if flag:
            return lower
        else:
            return -1