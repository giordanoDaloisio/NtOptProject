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
    scale = 25
    DrawG = pygv.AGraph(strict='true', splines='true')

    for i in G.nodes():
        pos = str(G.node[i]['x'] * scale) + ',' + str((G.node[i]['y']) * scale)

        if G.node[i]['load'] < 0:
            DrawG.add_node(i, shape='circle', pos=pos, label=G.node[i]['label'], color='red',
                           style='filled', fillcolor='salmon', fontsize='8', width='0.3')
        elif G.node[i]['load'] > 0:
            DrawG.add_node(i, shape='circle', pos=pos, label=G.node[i]['label'], color='green',
                           style='filled', fillcolor='palegreen1', fontsize='8', width='0.3')
        else:
            DrawG.add_node(i, shape='circle', pos=pos, label=G.node[i]['label'], fontsize='8', width='0.3')

    DrawG.layout(prog='neato', args='-n')
    if args.name:
        DrawG.draw(path=args.name + '.svg', format='svg')
    else:
        DrawG.draw('graph.svg')


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
        pos_x = random.randint(1, 40) + random.randint(1, 20)
        pos_y = random.randint(1, 40) + random.randint(1, 20)
        for i in range(1, abs(load) + 1):
            label = "%s,%s" % (station, i)
            G.add_node((station, i), station=station, load=load, label=label, x=pos_x, y=pos_y)
            nodes.append((station, i))
    return nodes


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="Name of the graph", type=str, required=False)
parser.add_argument("-dl", "--del_loads", help="Range of delivery vehicles for each delivery node", type=parse_range)
parser.add_argument("-pl", "--pick_loads", help="Range of pickup vehicles for each pickup node", type=parse_range)
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

G = nx.Graph()

# create the station visits nodes and connect them

dl_nodes = create_nodes(dl_stations)
pk_nodes = create_nodes(pk_stations)

for pk_node in pk_nodes:
    for dl_node in dl_nodes:
        u = (G.node[pk_node]['x'], G.node[pk_node]['y'])
        v = (G.node[dl_node]['x'], G.node[dl_node]['y'])
        d = euclidean_distance(u, v)
        time = d * 100
        G.add_edge(pk_node, dl_node, time=d)

# create the depot nodes and connect them

pos_x = random.randint(1, 30) + random.randint(1, 20)
pos_y = random.randint(1, 30) + random.randint(1, 20)
G.add_node(0, label=0, x=pos_x, y=pos_y, load=0)

pos_x = random.randint(1, 30) + random.randint(1, 20)
pos_y = random.randint(1, 30) + random.randint(1, 20)
G.add_node(1, label=1, x=pos_x, y=pos_y, load=0)

for node in pk_nodes:
    u = (G.node[0]['x'], G.node[0]['y'])
    v = (G.node[node]['x'], G.node[node]['y'])
    d = euclidean_distance(u, v)
    time = d * 100
    G.add_edge(0, node, time=d)

for node in dl_nodes:
    u = (G.node[node]['x'], G.node[node]['y'])
    v = (G.node[1]['x'], G.node[1]['y'])
    d = euclidean_distance(u, v)
    G.add_edge(node, 1, time=d)

draw_initial_graph()

if args.name:
    nx.write_graphml(G, args.name + '.gml')
else:
    nx.write_graphml(G, "graph.gml")
