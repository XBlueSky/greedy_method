from edge.edge import Edge
from fog_set.fog_set import Fog_Set
from constant.constant import Constant
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from argparse import ArgumentParser

parser = ArgumentParser(description= "Greedy Method")
parser.add_argument("filename", help="testcase file path")
args = parser.parse_args()

traffic_list    = []
# latency_list    = []
# total_cost      = []
# total_cost_un   = []
total_cost          = []
edge_cost           = []
fog_cost            = []

# Initial

# Constant: traffic, ratio, max_latency, least_error
constant = Constant(500, 0.01, 1, 1)

# Edge: capacity, max_servers, cost
edge = Edge(20, 10, 20)

# Fog_Set: ratio, edge_transmission_rate, fog_transmission_rate, capacity, total_fogs, testcase file
fogs_num = args.filename.split("_")
file_name = "testcase/"+args.filename
fog_set = Fog_Set(constant.ratio, 1250, 1250, 5, int(fogs_num[1]), file_name)

for t in range(100, 3000, 50):
# for l in [x * 0.01 for x in range(1, 200, 1)]:
    # for a in [0, 1]:
    # 0/1 knapsack problem with (1 − 1/ sqrt(e)) bound
    traffic = t
    # traffic = constant.traffic
    # latency = l
    latency = constant.max_latency
    bundle_list = []

    while traffic > constant.least_error:
        # Edge and all of fog would calculate its own maximum traffic
        if edge.used == False:
            edge.algorithm(traffic, latency, constant.least_error)
            bundle_list.append({'id': 'edge', 'traffic': edge.max_traffic, 'cost': edge.edge_cost(), 'CP': edge.max_traffic / edge.edge_cost(), 'chosen': False})

        for f in fog_set.fog_list:
            if f.used == False:
                f.algorithm(traffic, latency, constant.least_error)
                bundle_list.append({'id': f.index, 'traffic': f.max_traffic, 'cost': f.fog_cost(), 'CP': f.max_traffic / f.fog_cost(), 'chosen': False})

        if not bundle_list:
            # print("There is no enough capacity")
            break

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
        # if a == 0:
        #     another = max(bundle_list, key=lambda b : b['traffic'])

        #     if traffic_sum >= another['traffic']:
        #         traffic = traffic - traffic_sum
        #         for bundle in bundle_list:
        #             if bundle['chosen'] == True:
        #                 if bundle['id'] == 'edge':
        #                     edge.used = True
        #                 else:
        #                     fog_set.fog_list[bundle['id']].used = True
        #             else:
        #                 if bundle['id'] == 'edge':
        #                     edge.clear()
        #                 else:
        #                     fog_set.fog_list[bundle['id']].clear()
        #     else:
        #         traffic = traffic - another['traffic']
        #         for bundle in bundle_list:
        #             if bundle['id'] == another['id']:
        #                 if another['id'] == 'edge':
        #                     edge.used = True
        #                 else:
        #                     fog_set.fog_list[another['id']].used = True
        #             else:
        #                 if bundle['id'] == 'edge':
        #                     edge.clear()
        #                 else:
        #                     fog_set.fog_list[bundle['id']].clear()
        # else:
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
        bundle_list.clear()

    # latency_list.append(l)
    # if a == 0:
    #     total_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
    # else:
    # total_cost_un.append(edge.edge_cost() + fog_set.fog_set_cost())
    traffic_list.append(t)
    total_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
    edge_cost.append(edge.edge_cost())
    fog_cost.append(fog_set.fog_set_cost())
    edge.clear()
    fog_set.clear()

# output to static HTML file
output_file("graph/greddtORnot_traffic-cost_1.html")
# output_file("graph/latency-cost.html")

TOOLTIPS = [
        ("index", "$index"),
        ("traffic", "$x"),
        ("cost", "$y"),
    ]
# create a new plot with a title and axis labels
p = figure(plot_width=1600, plot_height=840, x_axis_label='Araival Traffic', y_axis_label='Cost', tooltips=TOOLTIPS)
# p = figure(plot_width=1600, plot_height=840, x_axis_label='Max latency', y_axis_label='Cost', tooltips=TOOLTIPS)
# p = figure(title="traffic to cost", x_axis_label='traffic', y_axis_label='cost')

# add a line renderer with legend and line thickness
# p.line(traffic_list, total_cost, legend="greedy.", line_width=3)
# p.line(traffic_list, total_cost_un, legend="unmodified greedy.", line_width=3, line_color="red")
p.line(traffic_list, total_cost, legend="total.", line_width=3)
p.line(traffic_list, edge_cost, legend="edge.", line_width=3, line_color="dodgerblue")
p.line(traffic_list, fog_cost, legend="fog.", line_width=3, line_color="deepskyblue")
# p.line(latency_list, total_cost, legend="greedy.", line_width=3)
# p.circle('x', 'y', size=7, source=source_mm1)
# p.circle('x', 'y', fill_color="red", line_color="red", size=7, source=source_mm2)
p.circle(traffic_list, total_cost, size=7)
p.circle(traffic_list, edge_cost, fill_color="dodgerblue", line_color="dodgerblue", size=7)
p.circle(traffic_list, fog_cost, fill_color="deepskyblue", line_color="deepskyblue", size=7)
# p.line(traffic_list, total_cost, legend="greedy.", line_width=2)

# show the results
show(p)


# edge.display()
# fog_set.display()