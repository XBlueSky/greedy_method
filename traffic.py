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

traffic_list        = []
# latency_list    = []
total_cost          = []
edge_cost           = []
fog_cost            = []
total_cost_fixed    = []
edge_cost_fixed     = []
fog_cost_fixed      = []
CP_cost             = []
cost_cost           = []
traffic_cost        = []

# Initial

# Constant: traffic, ratio, max_latency, least_error
constant = Constant(500, 0.01, 1, 1)

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
data['traffic'] = []

for t in range(100, 3000, 50):
    
    # edge.set_traffic(t)
    # fog_set.set_traffic(t)

    # for cost_type in ['fixed', 'diff']:
    for cost_type in ['diff']:
    # for algorithm_type in ['cost', 'traffic', 'CP']:
        # 0/1 knapsack problem with (1 − 1/ sqrt(e)) bound
        traffic = t
        bundle_list = []

        while traffic > constant.least_error:
            # Edge and all of fog would calculate its own maximum traffic
            if edge.used == False:
                edge.algorithm(traffic, constant.max_latency, constant.least_error)
                bundle_list.append({'id': 'edge', 'traffic': edge.max_traffic, 'cost': edge.edge_cost(), 'CP': edge.max_traffic / edge.edge_cost(), 'chosen': False})

            for f in fog_set.fog_list:
                if f.used == False:
                    f.algorithm(traffic, constant.max_latency, constant.least_error)
                    # if cost_type == 'fixed':
                    #     cost = f.fog_fixed_cost(25)
                    # else:
                    #     cost = f.fog_cost()
                    cost = f.fog_cost()
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
            # another = max(bundle_list, key=lambda b : b['traffic'])

            # if traffic_sum >= another['traffic']:
            #     traffic = traffic - traffic_sum
            #     for bundle in bundle_list:
            #         if bundle['chosen'] == True:
            #             if bundle['id'] == 'edge':
            #                 edge.used = True
            #             else:
            #                 fog_set.fog_list[bundle['id']].used = True
            #         else:
            #             if bundle['id'] == 'edge':
            #                 edge.clear()
            #             else:
            #                 fog_set.fog_list[bundle['id']].clear()
            # else:
            #     traffic = traffic - another['traffic']
            #     for bundle in bundle_list:
            #         if bundle['id'] == another['id']:
            #             if another['id'] == 'edge':
            #                 edge.used = True
            #             else:
            #                 fog_set.fog_list[another['id']].used = True
            #         else:
            #             if bundle['id'] == 'edge':
            #                 edge.clear()
            #             else:
            #                 fog_set.fog_list[bundle['id']].clear()
            
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

        if cost_type == 'fixed':
            total_cost_fixed.append(edge.edge_cost() + fog_set.fog_set_fixed_cost(25))
            edge_cost_fixed.append(edge.edge_cost())
            fog_cost_fixed.append(fog_set.fog_set_fixed_cost(25))
        else:
            # data['traffic'].append(str(t))
            # traffic_list.append(str(t))
            # for i, c in enumerate(collections):
            #     if i == 0:
            #         data[c].append(edge.max_traffic / t)
            #     else:
            #         if fog_set.fog_list[i - 1].max_traffic > 0:
            #             data[c].append(fog_set.fog_list[i - 1].max_traffic / t)
            #         else:
            #             data[c].append(0)
            # data['traffic'].append(str(t))
            # traffic_list.append(str(t))
            # for i, c in enumerate(collections):
            #     if i == 0:
            #         data[c].append(edge.active_servers)
            #     else:
            #         data[c].append(fog_set.fog_list[i - 1].used_vehicles)
            traffic_list.append(t)
            total_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
            edge_cost.append(edge.edge_cost())
            fog_cost.append(fog_set.fog_set_cost())
        
        # if algorithm_type == 'CP':
        #     traffic_list.append(t)
        #     CP_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
        # elif algorithm_type == 'cost':
        #     cost_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
        # else:
        #     traffic_cost.append(edge.edge_cost() + fog_set.fog_set_cost())
        
        # edge.display()
        # fog_set.display()

        edge.clear()
        fog_set.clear()

    
# output to static HTML file
# output_file("graph/traffic-cost.html")
output_file("graph/traffic/un-cost.html")

# p = figure(x_range=traffic_list, plot_width=1600, plot_height=900, title="traffic distribution",
#             tooltips="$name \ @$name")

# p.vbar_stack(collections, x='traffic', width=0.9, color=colors, source=data,
#              legend=[value(x) for x in collections])

# p.y_range.start = 0
# p.x_range.range_padding = 0.1
# p.xgrid.grid_line_color = None
# p.axis.minor_tick_line_color = None
# p.outline_line_color = None
# p.legend.location = "top_left"
# p.legend.orientation = "horizontal"

TOOLTIPS = [
        ("index", "$index"),
        ("traffic", "$x"),
        ("cost", "$y"),
    ]

# create a new plot with a title and axis labels
p = figure(plot_width=1600, plot_height=840, x_axis_label='Araival Traffic', y_axis_label='Cost', tooltips=TOOLTIPS)

# add a line renderer with legend and line thickness
p.line(traffic_list, total_cost, legend="total.", line_width=3)
p.line(traffic_list, edge_cost, legend="edge.", line_width=3, line_color="dodgerblue")
p.line(traffic_list, fog_cost, legend="fog.", line_width=3, line_color="deepskyblue")
# p.line(traffic_list, total_cost_fixed, legend="total-fixed.", line_width=3, line_color="red")
# p.line(traffic_list, edge_cost_fixed, legend="edge-fixed.", line_width=3, line_color="tomato")
# p.line(traffic_list, fog_cost_fixed, legend="fog-fixed.", line_width=3, line_color="pink")
# p.line(traffic_list, CP_cost, legend="CP.", line_width=3)
# p.line(traffic_list, cost_cost, legend="cost.", line_width=3, line_color="#e84d60")
# p.line(traffic_list, traffic_cost, legend="traffic.", line_width=3, line_color="lightseagreen")


p.circle(traffic_list, total_cost, size=7)
p.circle(traffic_list, edge_cost, fill_color="dodgerblue", line_color="dodgerblue", size=7)
p.circle(traffic_list, fog_cost, fill_color="deepskyblue", line_color="deepskyblue", size=7)
# p.circle(traffic_list, total_cost_fixed, fill_color="red", line_color="red", size=7)
# p.circle(traffic_list, edge_cost_fixed, fill_color="tomato", line_color="tomato", size=7)
# p.circle(traffic_list, fog_cost_fixed, fill_color="pink", line_color="pink", size=7)
# p.circle(traffic_list, CP_cost, size=7)
# p.circle(traffic_list, cost_cost, fill_color="#e84d60", line_color="#e84d60", size=7)
# p.circle(traffic_list, traffic_cost, fill_color="lightseagreen", line_color="lightseagreen", size=7)


# show the results
show(p)


