import random
from argparse import ArgumentParser

# do argument parser
parser = ArgumentParser()
parser.add_argument("fog_num", help="Input number of fogs")
parser.add_argument("cost", help="Input fixed cost number or diff")
args = parser.parse_args()

with open("../testcase/fog_" + args.fog_num, 'w') as fp:

    for i in range(int(args.fog_num)):
        vehicle_num = random.randint(1, 100)

        # cost
        if args.cost == "diff":
            for v in range(vehicle_num):
                diff_cost = random.randint(1, 100)
                fp.write(str(diff_cost) + " ")
        else:
            for v in range(vehicle_num):
                fp.write(args.cost + " ")
        fp.write("\n")

        # consumptoin rate
        for v in range(vehicle_num):
            consumption_rate = random.randint(1, 9)
            fp.write(str(consumption_rate) + " ")
        fp.write("\n")

        # power constraint
        initial_power       = []
        threshold_power     = []
        for v in range(vehicle_num):
            initial = random.randint(30, 100)
            threshold = random.randint(10, 50)
            if initial < threshold:
                initial_power.append(threshold)
                threshold_power.append(initial)
            elif initial > threshold:
                initial_power.append(initial)
                threshold_power.append(threshold)
            else:
                initial_power.append(initial+1)
                threshold_power.append(threshold)
        for v in range(vehicle_num):
            fp.write(str(initial_power[v]) + " ")
        fp.write("\n")
        for v in range(vehicle_num):
            fp.write(str(threshold_power[v]) + " ")
        fp.write("\n")



