import networkx as nx
import matplotlib.pyplot as plt
import random
import igraph as ig
import time
import pandas as pd
import numpy as np
import csv
import math

def commmunities(graph, method):
    """"Presenting a number of community detection algorithms"""

    graph = graph.as_undirected("each") #Changing the networks from directed to undirected. The infomap algorithm could not create proper communities, therefore it was decided that the multilevel algorithm should be used instead, this however requires the network to be undirected.

    # EDGE_BETWEENNESS most exact but also slowest and most computer heavy
    # time = 946.8 s (edge) + 353.9 s (vertex)
    if method == 'edge_betweenness':
        v = graph.community_edge_betweenness()

    # INFOMAP this one should specifically be for directed graphs but im not sure if we need to detect communities with the graph being directed
    if method == 'infomap':
        v = graph.community_infomap()

    # FAST_GREEDY & MULITLEVEL (very similar) fast and accurate, Multilevel should perform very well
    if method == 'fast_greedy':
        v = graph.community_fastgreedy()
    elif method == 'multilevel':
        v = graph.community_multilevel()

    # WALKTRAP less fast than FAST_GREEDY but slightly more accurate
    if method == 'walktrap':
        v = graph.community_walktrap()

    # LEIDEN algorithm should also be good but only for undirected graphs
    if method == 'leiden':
        v = graph.community_leiden()

    return v


def plot(graph, membership=None):
    """"This function gives identical styling to each node within one community and it makes the edges between communities gray in color"""
    if membership is not None:
        gcopy = graph.copy()
        edges = []
        edges_colors = []
        for edge in graph.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append('green')
            else:
                edges_colors.append("red")
        gcopy.delete_edges(edges)
        layout = gcopy.layout(None)
        graph.es["color"] = edges_colors
    else:
        layout = g.layout(None)
        graph.es["color"] = "gray"

    """"Creating empty lists for the layout of the visualization"""
    airports = []
    coords = []

    """"Reading the coördinates of the airports for the layout"""
    with open("C:\\Users\\phili\\PycharmProjects\\Test-Analysis-Simulation\\Assets\\Airports.csv",
              encoding="mbcs") as file:
        reader = csv.reader(file, delimiter=",")
        i = 0
        for row in reader:
            for name in g.vs["name"]:
                if row[1] == name:
                    airports.append(row[1])
                    coords.append((float(row[-2]), -float(row[-3])))
                    i += 1
    lout = coords

    """"Determining the visual aspects of the network"""
    visual_style = {}
    visual_style["edge_arrow_size"] = 0.025
    visual_style["vertex_shape"] = "circle"
    visual_style['layout'] = lout
    visual_style["vertex_size"] = [50 * math.log(graph.degree(i)) for i in graph.vs]
    visual_style['layout'] = lout
    visual_style["edge_width"] = [0.01 * int(weight) for weight in graph.es["weight"]]
    visual_style["bbox"] = (15000, 15000)
    visual_style["margin"] = 40
    visual_style["edge_label"] = graph.es["weight"]
    g.vs["label"] = g.vs["name"]

    if membership is not None:
        #only need the code below for random colors
        colorsrand = [] #'b','g','r','c','m','y'
        colors = ['Tomato','Orange', 'DodgerBlue', 'MediumSeaGreen', 'SlateBlue', "Violet", "#FF3399", "#9CCC65", "#00838F", "#795548"]
        for i in range(0, max(membership) + 1):
            colorsrand.append('%06X' % np.random.randint(0, 0xFFFFFF))
        for vertex in graph.vs():
            # vertex["color"] = str('#') + colorsrand[membership[vertex.index]]
            vertex["color"] = colors[membership[vertex.index]]
        visual_style["vertex_color"] = graph.vs["color"]
    ig.plot(graph, autocurve= False, **visual_style)

if __name__ == "__main__":
    """"Runtime"""
    start_time = time.time()

    """"Specifying the filename and location"""
    filename = "EU_flights_2019_06.csv"
    path = f'C:\\Users\\phili\\PycharmProjects\\Test-Analysis-Simulation\\2019_Filtered\\{filename}'

    """Creating a graph from data"""
    data = pd.read_csv(path, usecols=[1, 2])
    g0 = ig.Graph.DataFrame(edges=data, directed=True)

    """Creating a weighted graph from the adjacency matrix"""
    adj_matrix = g0.get_adjacency()
    adj_matrix = list(adj_matrix)
    g = ig.Graph.Weighted_Adjacency(adj_matrix)
    g.vs["name"] = g0.vs["name"]

    """"Presenting options for which type of community detection algorithm should be used"""
    methods = ["edge_betweenness", "infomap", "fast_greedy", "multilevel", "walktrap", "leiden"]
    clusters = commmunities(g, methods[3]) #According to the research presented in the method section of the paper, we should use the multilevel algorithm
    print(clusters.modularity) #This number gives a representation of how good the communities have been formed, if this number is close to 0, then the communities which have been found are not good communities
    print(clusters) #Printing the actual communities
    membership = clusters.membership
    plot(g, membership)

    """"Runtime"""
    print(time.time() - start_time)

# source of code which helped with visualisation
# https://stackoverflow.com/questions/23184306/draw-network-and-grouped-vertices-of-the-same-community-or-partition
