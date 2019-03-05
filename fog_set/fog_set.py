from fog_set.fog import Fog
import prettytable as pt

class Fog_Set:
    fog_list            = []
    def __init__(self, traffic, ratio, edge_transmission_rate, fog_transmission_rate, capacity, total_fogs, file_name):
        self.total_traffic      = traffic
        self.ratio              = ratio
        self.total_fogs         = total_fogs
        # self.max_vehicles       = max(vehicle_num_in_fogs)
        # for index, vehicle_num in enumerate(vehicle_num_in_fogs):
        vehicle_num_in_fogs = []    
        file = open(file_name,'r')
        for i,line in enumerate(file):
            if i % 4 == 0:
                cost_set = list( map( int, line.split()))
            elif i % 4 == 1:
                consumption_rate_set = list( map( int, line.split()))
            elif i % 4 == 2:
                initial_power_set = list( map( int, line.split()))
            else:
                threshold_power_set = list( map( int, line.split()))
                index = i // 4
                vehicle_num_in_fogs.append(len(cost_set))
                self.fog_list.append( Fog(index, capacity, vehicle_num_in_fogs[index], edge_transmission_rate, fog_transmission_rate))
                self.fog_list[index].set_vehicle_set(cost_set, consumption_rate_set, initial_power_set, threshold_power_set)
        self.max_vehicles = max(vehicle_num_in_fogs)

    def used_bits_table(self):
        return [f.used_bits_list() for f in sorted(self.fog_list, key=lambda f : f.index)]

    def fog_set_cost(self):
        return sum([f.fog_cost() for f in self.fog_list])

    # def algorithm(self, traffic, max_latency, least_error):

    #     # All of fog would calculate its own maximum traffic
    #     bundle_list = []
    #     for index, f in enumerate(self.fog_list):
    #         f.algorithm(traffic, max_latency, least_error)
    #         bundle = [index + 1, f.max_traffic, f.fog_cost()]
    #         bundle_list.append(bundle)
    #     return bundle_list

        # Start from the fog where there are most vehicles
        # self.fog_list.sort(key=lambda f : f.total_vehicles, reverse=True)
        # for f in self.fog_list:
        #     f.algorithm(traffic, max_latency, least_error)
        #     traffic = traffic - f.max_traffic
        #     if traffic == 0:
        #         return True
        # return False
    

    def display(self):
        self.fog_list.sort(key=lambda f : f.index)
        table = pt.PrettyTable()
        table.add_column("Index", ["Traffic", "Probability", "Used vehicles", "Cost", "Latency"])
        for f in self.fog_list:
            table.add_column (str(f.index), [f.max_traffic, f.max_traffic / self.total_traffic, f.used_vehicles, f.fog_cost(), f.latency])
        print("Fog")
        print(table)
        used_bits_table = pt.PrettyTable()
        used_bits_table.add_column("Vehicles / Fog", [str(i) for i in range(self.max_vehicles)])
        for index, f in enumerate(self.used_bits_table()):
            f = [int(i) for i in f]
            f.extend(["N/A"] * (self.max_vehicles - len(f)))
            used_bits_table.add_column(str(index), f)
        print(used_bits_table)