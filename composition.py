from edge.edge import Edge
from fog_set.fog_set import Fog_Set
from constant.constant import Constant
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
import random
from argparse import ArgumentParser

# parser = ArgumentParser(description= "Greedy Method")
# parser.add_argument("filename", help="testcase file path")
# args = parser.parse_args()

# Initial

# Constant: traffic, ratio, max_latency, least_error
constant = Constant(500, 0.01, 1, 1)

# Edge: capacity, max_servers, cost
edge = Edge(200, 5, 200)

cost_list = []
vehicle_num_list = []
usage_time_list = []
for i in range(10):
    # Fog_Set: ratio, edge_transmission_rate, fog_transmission_rate, capacity, total_fogs, testcase file
    # fogs_num = args.filename.split("_")
    # file_name = "testcase/"+args.filename
    # fog_set = Fog_Set(constant.ratio, 1250, 1250, 125, 5, int(fogs_num[1]), file_name)
    fog_set = Fog_Set(constant.ratio, 1250, 1250, 125, 5, 10, "testcase/Efog_10_v" + str(i+1))

    cost = []
    vehicle_num = []
    usage_time = []
    
    for f in fog_set.fog_list:
        # total_cost = sum([v.cost for v in f.vehicle_set])
        # cost.append(total_cost / f.total_vehicles)
        total_usage_time = sum([v.usage_time for v in f.vehicle_set])
        usage_time.append(total_usage_time / f.total_vehicles)
        vehicle_num.append(f.total_vehicles)

    # cost_list.append(cost)
    usage_time_list.append(usage_time)
    vehicle_num_list.append(vehicle_num)

data = dict()
data['fogs'] = []
# data['cost'] = []
data['usage_time'] = []
data['vehicle_num'] = []
for f in fog_set.fog_list:
    data['fogs'].append("F" + str(f.index))
    # data['cost'].append(sum([c[f.index] for c in cost_list]) / len(cost_list))
    data['usage_time'].append(sum([u[f.index] for u in usage_time_list]) / len(usage_time_list))
    data['vehicle_num'].append(sum([v[f.index] for v in vehicle_num_list]) / len(vehicle_num_list))

source = ColumnDataSource(data=data)
# output to static HTML file
# output_file("graph/traffic-cost.html")
output_file("graph/E_fog/composition/average_composition.html")

p = figure(x_range=data['fogs'], y_range=(0, 100), plot_width=1600, plot_height=900, title="vehicular-fog composition",
           toolbar_location=None, tools="")

# p.vbar(x=dodge('fogs', -0.2, range=p.x_range), top='cost', width=0.3, source=source,
    #    color="#e84d60", legend=value("cost"))

p.vbar(x=dodge('fogs', -0.2, range=p.x_range), top='usage_time', width=0.3, source=source,
       color="#e84d60", legend=value("usage_time"))

p.vbar(x=dodge('fogs',  0.2,  range=p.x_range), top='vehicle_num', width=0.3, source=source,
       color="#718dbf", legend=value("vehicle_num"))

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

# show the results
show(p)


