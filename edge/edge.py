from m_m_c.m_m_c import m_m_c_latency
import prettytable as pt
import math

class Edge:
    used                = False
    active_servers      = 0
    max_traffic         = 0
    latency             = 0

    def __init__(self, capacity, max_servers, cost):
        self.capacity           = capacity
        self.max_servers        = max_servers
        self.cost               = cost
    
    def set_traffic(self, traffic):
        self.total_traffic      = traffic

    def computation_latency(self, traffic, active_servers):
        # check number of servers constraint
        if active_servers <= self.max_servers:
            return m_m_c_latency(active_servers, traffic, self.capacity)
        else:
            return -1

    def edge_cost(self):
        return self.active_servers * self.cost

    def clear(self):
        self.active_servers     = 0
        self.max_traffic        = 0
        self.latency            = 0
        self.used               = False
        
    # local computation in edge
    def algorithm(self, traffic, max_latency, least_error):
        
        # start from maximum servers
        active_servers = self.max_servers

        # find maximum traffic
        # check arrival traffic is larger than the traffic that can be handle in edge
        if self.computation_latency(traffic, active_servers) > max_latency:

            # bisection method variation
            self.max_traffic = self.bisection_method(traffic, active_servers, max_latency, least_error)

            # interpolation search variation
            # self.max_traffic = self.interpolation_search(traffic, active_servers, max_latency, least_error)
        else:
            self.max_traffic = traffic

        # find minmum number of active servers to handle the traffic
        # linear search
        while self.computation_latency(self.max_traffic, active_servers) <= max_latency:
            active_servers = active_servers - 1 
        
        self.active_servers = active_servers + 1
        self.latency = self.computation_latency(self.max_traffic, self.active_servers)
        # return [0, self.max_traffic, self.edge_cost()]
        # gradient descent

    def bisection_method(self, traffic, active_servers, max_latency, least_error):
        lower   = 1
        upper   = traffic
        flag    = False

        while (lower + least_error) <= upper:
            mid = (lower + upper) / 2
            total_latency = self.computation_latency(mid, active_servers)

            if total_latency <= max_latency:
                flag    = True
                lower   = mid
            else:
                upper   = mid

        if flag:
            return lower
        else:
            return -1

    def interpolation_search(self, traffic, active_servers, max_latency, least_error):
        lower   = 1
        upper   = traffic
        flag    = False

        while (lower + least_error) <= upper:
            slope = (max_latency - self.computation_latency(lower, active_servers)) / (self.computation_latency(upper, active_servers) - self.computation_latency(lower, active_servers))
            mid = (upper - lower) * slope + lower
            total_latency = self.computation_latency(mid, active_servers)

            if mid < lower or mid > upper:
                break
            if total_latency <= max_latency:
                flag    = True
                lower   = mid
            else:
                upper   = mid
        
        if flag:
            return lower
        else:
            return -1

    def display(self):
        table = pt.PrettyTable()
        table.field_names = ["Traffic", "Offloading Probability", "Active servers number", "Cost", "Latency"]
        table.add_row([self.max_traffic, self.max_traffic / self.total_traffic, self.active_servers, self.edge_cost(), self.latency])
        print("Edge")
        print(table)