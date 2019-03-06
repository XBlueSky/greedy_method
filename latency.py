from edge.edge import Edge
from fog_set.fog_set import Fog_Set
from constant.constant import Constant
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.core.properties import value
import random
from argparse import ArgumentParser

parser = ArgumentParser(description= "Greedy Method")
parser.add_argument("filename", help="testcase file path")
args = parser.parse_args()

# traffic_list        = []
latency_list        = []
total_cost          = []
edge_cost           = []
fog_cost            = []
total_cost_fixed    = []
edge_cost_fixed     = []
fog_cost_fixed      = []
# CP_cost             = []
# cost_cost           = []
# traffic_cost        = []

# Initial

# Constant: traffic, ratio, max_latency, least_error
constant = Constant(1000, 0.01, 1, 1)

# Edge: capacity, max_servers, cost
edge = Edge(20, 10, 20)

# Fog_Set: ratio, edge_transmission_rate, fog_transmission_rate, capacity, total_fogs, testcase file
fogs_num = args.filename.split("_")
file_name = "testcase/"+args.filename
fog_set = Fog_Set(constant.ratio, 1250, 1250, 5, int(fogs_num[1]), file_name)

collections = ["edge_10"]
colors      = ['#0D3331', 'darkslategray', "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
for f in fog_set.fog_list:
    collections.append("F" + str(f.index) + "_" + str(f.total_vehicles))
data = dict((c,[]) for c in collections)
data['latency'] = []

for l in [x * 0.01 for x in range(1, 100, 2)]:

    # for cost_type in ['fixed', 'diff']:
    for cost_type in ['diff']:
    # for algorithm_type in ['cost', 'traffic', 'CP']:
        # 0/1 knapsack problem with (1 − 1/ sqrt(e)) bound
        traffic = constant.traffic
        latency = l
        bundle_list = []

        while traffic > constant.least_error:
            # Edge and all of fog would calculate its own maximum traffic
            if edge.used == False:
                edge.algorithm(traffic, latency, constant.least_error)
                bundle_list.append({'id': 'edge', 'traffic': edge.max_traffic, 'cost': edge.edge_cost(), 'CP': edge.max_traffic / edge.edge_cost(), 'chosen': False})

            for f in fog_set.fog_list:
                if f.used == False:
                    f.algorithm(traffic, latency, constant.least_error)
                    if cost_type == 'fixed':
                        cost = f.fog_fixed_cost(25)
                    else:
                        cost = f.fog_cost()
                    # cost = f.fog_cost()
                    bundle_list.append({'id': f.index, 'traffic': f.max_traffic, 'cost': cost, 'CP': f.max_traffic / cost, 'chosen': False})

            if not bundle_list:
                # print("There is no enough capacity")
                break

            # Sort by CP value
            # if algorithm_type == 'CP':
            #     bundle_list.sort(key=lambda b : b['CP'], reverse=True)
            # elif algorithm_type == 'cost':
            #     bundle_list.sort(key=lambda b : b['cost'], reverse=False)
            # else:
            #     bundle_list.sort(key=lambda b : b['traffic'], reverse=True)
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

        if cost_type == 'fixed':
            # latency_list.append(l)
            total_cost_fixed.append(edge.edge_cost() + fog_set.fog_set_fixed_cost(25))
            edge_cost_fixed.append(edge.edge_cost())
            fog_cost_fixed.append(fog_set.fog_set_fixed_cost(25))
        else:
            data['latency'].append('{:10.2f}'.format(l))
            latency_list.append('{:10.2f}'.format(l))
            for i, c in enumerate(collections):
                if i == 0:
                    data[c].append(edge.max_traffic / constant.traffic)
                else:
                    if fog_set.fog_list[i - 1].max_traffic > 0:
                        data[c].append(fog_set.fog_list[i - 1].max_traffic / constant.traffic)
                    else:
                        data[c].append(0)
            # data['latency'].append('{:10.2f}'.format(l))
            # latency_list.append('{:10.2f}'.format(l))
            # for i, c in enumerate(collections):
            #     if i == 0:
            #         data[c].append(edge.active_servers)
            #     else:
            #         data[c].append(fog_set.fog_list[i - 1].used_vehicles)
            # latency_list.append('{:10.2f}'.format(l))
            # total_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
            # edge_cost.append(edge.edge_cost())
            # fog_cost.append(fog_set.fog_set_cost())
        
        # if algorithm_type == 'CP':
        #     latency_list.append(l)
        #     CP_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
        # elif algorithm_type == 'cost':
        #     cost_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
        # else:
        #     traffic_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
        edge.clear()
        fog_set.clear()

# output to static HTML file
output_file("graph/latency/traffic-distribution_1000.html")

p = figure(x_range=latency_list, plot_width=1600, plot_height=900, title="1000 traffic distribution",
            tooltips="$name \ @$name")

p.vbar_stack(collections, x='latency', width=0.9, color=colors, source=data,
             legend=[value(x) for x in collections])

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

# TOOLTIPS = [
#         ("index", "$index"),
#         ("traffic", "$x"),
#         ("cost", "$y"),
#     ]
# create a new plot with a title and axis labels
# p = figure(plot_width=1600, plot_height=840, x_axis_label='Max latency', y_axis_label='Cost', tooltips=TOOLTIPS)
# p = figure(title="traffic to cost", x_axis_label='traffic', y_axis_label='cost')

# add a line renderer with legend and line thickness
# p.line(latency_list, total_cost, legend="total.", line_width=3)
# p.line(latency_list, edge_cost, legend="edge.", line_width=3, line_color="dodgerblue")
# p.line(latency_list, fog_cost, legend="fog.", line_width=3, line_color="deepskyblue")
# p.line(latency_list, total_cost_fixed, legend="total-fixed.", line_width=3, line_color="red")
# p.line(latency_list, edge_cost_fixed, legend="edge-fixed.", line_width=3, line_color="tomato")
# p.line(latency_list, fog_cost_fixed, legend="fog-fixed.", line_width=3, line_color="pink")
# p.line(latency_list, CP_cost, legend="CP.", line_width=3)
# p.line(latency_list, cost_cost, legend="cost.", line_width=3, line_color="#e84d60")
# p.line(latency_list, traffic_cost, legend="traffic.", line_width=3, line_color="lightseagreen")


# p.circle(latency_list, total_cost, size=7)
# p.circle(latency_list, edge_cost, fill_color="dodgerblue", line_color="dodgerblue", size=7)
# p.circle(latency_list, fog_cost, fill_color="deepskyblue", line_color="deepskyblue", size=7)
# p.circle(latency_list, total_cost_fixed, fill_color="red", line_color="red", size=7)
# p.circle(latency_list, edge_cost_fixed, fill_color="tomato", line_color="tomato", size=7)
# p.circle(latency_list, fog_cost_fixed, fill_color="pink", line_color="pink", size=7)
# p.circle(latency_list, CP_cost, size=7)
# p.circle(latency_list, cost_cost, fill_color="#e84d60", line_color="#e84d60", size=7)
# p.circle(latency_list, traffic_cost, fill_color="lightseagreen", line_color="lightseagreen", size=7)


# show the results
show(p)


# edge.display()
# fog_set.display()