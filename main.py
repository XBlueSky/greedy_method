from edge.edge import Edge
from fog_set.fog_set import Fog_Set
from constant.constant import Constant
# from argparse import ArgumentParser

# parser = ArgumentParser(description= "Greedy Method")
# parser.add_argument("filename", help="file path")
# args = parser.parse_args()

# Initial

# Constant: traffic, ratio, max_latency, least_error
constant = Constant(5000, 0.01, 1, 1)

# Edge: capacity, max_servers, cost
edge = Edge(constant.traffic, 1000, 3, 10)

# Fog_Set: ratio, edge_transmission_rate, fog_transmission_rate, capacity, total_fogs, vehicle_num_in_fogs = []
fog_set = Fog_Set(constant.traffic, constant.ratio, 10000, 3000, 300, 2, [3,5])
fog_set.input("testcase/small")

# 0/1 knapsack problem with (1 − 1/ sqrt(e)) bound
traffic = constant.traffic
bundle_list = []

while traffic > 0:
    # Edge and all of fog would calculate its own maximum traffic
    if edge.used == False:
        edge.algorithm(traffic, constant.max_latency, constant.least_error)
        bundle_list.append({'id': 'edge', 'traffic': edge.max_traffic, 'cost': edge.edge_cost(), 'CP': edge.max_traffic / edge.edge_cost(), 'chosen': False})

    for f in fog_set.fog_list:
        if f.used == False:
            f.algorithm(traffic, constant.max_latency, constant.least_error)
            bundle_list.append({'id': f.index, 'traffic': f.max_traffic, 'cost': f.fog_cost(), 'CP': f.max_traffic / f.fog_cost(), 'chosen': False})
    
    # Sort by CP value
    bundle_list.sort(key=lambda b : b['CP'], reverse=True)
    traffic_sum = 0
    for bundle in bundle_list:
        if traffic_sum + bundle['traffic'] <= traffic:
            traffic_sum = traffic_sum + bundle['traffic']
            bundle['chosen'] = True
        else:
            break

    # The modified point
    another = max(bundle_list, key=lambda b : b['traffic'])

    if traffic_sum >= another['traffic']:
        traffic = traffic - traffic_sum
        for bundle in bundle_list:
            if bundle['chosen'] == True:
                if bundle['id'] == 'edge':
                    edge.used = True
                else:
                    fog_set.fog_list[bundle['id']].used = True
            else:
                if bundle['id'] == 'edge':
                    edge.clear()
                else:
                    fog_set.fog_list[bundle['id']].clear()
    else:
        traffic = traffic - another['traffic']
        for bundle in bundle_list:
            if bundle['id'] == another['id']:
                if another['id'] == 'edge':
                    edge.used = True
                else:
                    fog_set.fog_list[another['id']].used = True
            else:
                if bundle['id'] == 'edge':
                    edge.clear()
                else:
                    fog_set.fog_list[bundle['id']].clear()
    bundle_list.clear()

edge.display()
fog_set.display()