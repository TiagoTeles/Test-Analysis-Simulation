import igraph as ig
import time
import pandas as pd
import numpy as np
import csv
import math

""""Runtime"""
start_time = time.time()

GIT_DIR = __file__[0:-21]
ASSET_DIR = GIT_DIR + "Assets/"
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020  = GIT_DIR + "2020_Filtered/"
FLIGHT_DIR = "EU_flights_2020_01.csv"
AIRPORT_DIR = "Airports.csv"


"""Creating a graph from data"""
data = pd.read_csv(DIR_2020 + FLIGHT_DIR, usecols=[1,2])
g0 = ig.Graph.DataFrame(edges=data,directed=True)


"""Creating a weighted graph from the adjacency matrix"""

adj_matrix = g0.get_adjacency()
adj_matrix = list(adj_matrix)

g = ig.Graph.Weighted_Adjacency(adj_matrix)
g.vs["name"] = g0.vs["name"]

"""Getting the coordinates of airports for the layout"""

airports = []
coords = []


with open(ASSET_DIR + AIRPORT_DIR, encoding="utf8") as file:
    reader = csv.reader(file, delimiter = ",")
    i = 0
    for row in reader:
        for name in g.vs["name"]:
            if row[1] == name:
                airports.append(row[1])
                coords.append((float(row[-2]),float(row[-3])))
                i += 1


""""Checks and experiments"""

# print(airports)
# print(coords)
# print(len(g.vs["name"]), len(airports))

# print(g)
# print(adj_matrix)
# print(np.shape(adj_matrix))
# print(g0.is_weighted())
# print(type(adj_matrix))

# print(g.get_adjacency())
# print(g.is_weighted())
# print(g.es.attributes())

# for i in range(len(g.vs["name"])):
#     print(g.vs[i].attributes(),g.degree(i))
print(g.vs.select(_degree=g.maxdegree())["name"])

# for j in range(len(g.es["weight"])):
#     print(int(g.es[j]["weight"]))

bigedge = g.es.select(weight_gt = 100)
print(len(bigedge))

tuple_lst = []
coords_lst = []

for e in g.es:
    if int(e["weight"]) > 0:
        tuple_lst.append(e.tuple)

for tp in tuple_lst:
    coords_lst.append((coords[tp[0]], coords[tp[1]]))

"""Plotting the graph"""

lout = coords
g.vs["label"] = g.vs["name"]

"""Visual properties of the graph, scalable size of vertices, edges etc."""

visuals = {}
visuals["vertex_size"] = [10 * math.log(g.degree(i)) for i in g.vs]
visuals["edge_width"] = [int(weight)//100 for weight in g.es["weight"]]
visuals["edge_arrow_size"] = 0.5


ig.plot(g, layout = lout, bbox = (5000,5000), **visuals)

"""Runtime"""
print(time.time() - start_time)