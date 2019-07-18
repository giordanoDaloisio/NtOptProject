import networkx as nx
import pygraphviz as pygv
import argparse
from argparse import ArgumentTypeError
import random


def euclidean_distance(u, v):
    return int((((int(u[0]) - int(v[0])) ** 2 + (int(u[1]) - int(v[1])) ** 2) ** 0.5) * 100)


def parse_range(string):
    m = string.split('-')
    if not m:
        raise ArgumentTypeError(string + " is not a range of number. Expected forms like '0-5'.")
    if int(m[0]) > int(m[1]):
        raise ArgumentTypeError(string + ": wrong range. Expected forms like '0-5'.")
    return int(m[0]), int(m[1])


def draw_initial_graph():
    global DrawG
    scale = 50
    DrawG = pygv.AGraph(directed=True, strict='true', splines='true')

    for i in G.nodes():
        pos = str(G.node[i]['x'] * scale) + ',' + str((G.node[i]['y']) * scale)
        DrawG.add_node(i, shape='circle', pos=pos, label=G.node[i]['label'])

    DrawG.layout(prog='neato', args='-n')
    if args.name:
        DrawG.draw(path=args.name + '.png', format='png')
    else:
        DrawG.draw('graph.png')


def create_stations(n, lb, ub):
    stations = []
    for station in range(1, n):
        stations.append(
            {"station": station,
             "load": random.randint(lb, ub)
             }
        )
    return stations


def create_nodes(stations):
    nodes = []
    for elem in stations:
        station = elem['station']
        load = elem['load']
        for i in range(1, abs(load) + 1):
            label = "(%s, %s)" % (station, i)
            pos_x = random.randint(1, 100) + random.randint(1, 50) - random.randint(1, 25)
            pos_y = random.randint(1, 100) + random.randint(1, 50) - random.randint(1, 25)
            G.add_node((station, i), station=station, load=load, label=label, x=pos_x, y=pos_y)
            nodes.append((station, i))

    return nodes


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="Name of the graph", type=str, required=False)
parser.add_argument("-dl", "--del_loads", help="Range of delivery vehicles for each node", type=parse_range)
parser.add_argument("-pl", "--pick_loads", help="Range of pickup vehicles for each node", type=parse_range)
parser.add_argument("-ds", "--delivery_stations", help="Number of delivery stations", type=int)
parser.add_argument("-ps", "--pickup_stations", help="Number of pickup stations", type=int)
args = parser.parse_args()

# create the stations and define the full vehicle loads for each station

pk_stations = [
    {'station': station,
     'load': random.randint(args.pick_loads[0], args.pick_loads[1])}
    for station in range(1, args.pickup_stations + 1)
]

dl_stations = [
    {'station': station,
     'load': -random.randint(args.del_loads[0], args.del_loads[1])}
    for station in range(args.pickup_stations + 1, args.pickup_stations+args.delivery_stations + 1)
]

# create the graph

G = nx.DiGraph()

dl_nodes = create_nodes(dl_stations)
pk_nodes = create_nodes(pk_stations)
