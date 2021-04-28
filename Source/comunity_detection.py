import networkx as nx
import matplotlib.pyplot as plt
import random
import igraph as ig
import time
import pandas as pd
import numpy as np
import csv
import math
import cartopy as cp
from data_visualization import get_coordinates

# General settings
GIT_DIR = __file__[0:-28]
ASSET_DIR = GIT_DIR + "Assets/"
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020  = GIT_DIR + "2020_Filtered/"
FLIGHT_DIR = "EU_flights_2020_01.csv"
AIRPORT_DIR = "Airports.csv"

# Caropy settings
COLOUR_OCEAN = (1, 1, 1)
COLOUR_LAND = (0.9, 0.9, 0.9)
MAP_BOUNDS = (-30, 60, 25, 70)
PROJECTION = cp.crs.PlateCarree()
TRANSFORM = cp.crs.Geodetic()

# IGraph settings
AS = 0.5
RES = (5760, 5760/1.8)


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


def plot(graph, filename, membership=None):
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
    visual_style["vertex_size"] = [50 * math.log(graph.degree(i)) for i in graph.vs]
    visual_style['layout'] = lout
    visual_style["edge_width"] = [0.01 * int(weight) for weight in graph.es["weight"]]
    visual_style["bbox"] = (15000, 15000)
    visual_style["margin"] = 40
    visual_style["edge_label"] = graph.es["weight"]
    g.vs["label"] = g.vs["name"]

    if membership is not None:
        colors = ['Tomato','Orange', 'DodgerBlue', 'MediumSeaGreen', 'SlateBlue', "Violet", "#FF3399", "#9CCC65", "#00838F", "#795548"]
        for vertex in graph.vs():
            vertex["color"] = colors[membership[vertex.index]]
        visual_style["vertex_color"] = graph.vs["color"]
    # ig.plot(graph, f'{filename}.png', autocurve= False, **visual_style)
    ig.plot(graph, autocurve= False, **visual_style)
    return graph, visual_style

# def display_map(graph, coords, membership, line_width = 0.01, marker_size = 1, colour = "Black"):
#     """
#     Displays a map with the provided data using
#     matplotlib using the provided settings.
#
#     Arguments:
#         graph (Graph): Graph of the network
#         coordinates (List): List of OD coordinate pairs
#         line_width (float): Line width
#         marker_size (float): Marker size
#         colour (Tuple): Line and marker colour
#     """
#
#     # Determine list of used airports
#     coordinates = []
#     for airport in coords:
#         for name in graph.vs["name"]:
#             if airport[0] == name:
#                 coordinates.append((airport[1], airport[2]))
#
#     # Set projection
#     axes = plt.axes(projection = PROJECTION)
#
#     # Map settings
#     grid = axes.gridlines(draw_labels = True)
#     axes.coastlines(resolution="50m")
#     axes.set_extent(MAP_BOUNDS)
#
#     # Map features
#     axes.add_feature(cp.feature.BORDERS, linestyle='--', alpha=1)
#     axes.add_feature(cp.feature.LAND, facecolor=COLOUR_LAND)
#     axes.add_feature(cp.feature.OCEAN, facecolor=COLOUR_OCEAN)
#     axes.add_feature(cp.feature.LAKES, facecolor=COLOUR_OCEAN)
#
#     # Plot features
#     grid.xlabel_style = {"size": 12}
#     grid.ylabel_style = {"size": 12}
#     grid.xformatter = cp.mpl.gridliner.LONGITUDE_FORMATTER
#     grid.yformatter = cp.mpl.gridliner.LATITUDE_FORMATTER
#     grid.bottom_labels = False
#     grid.left_labels = False
#
#     # Add labels
#     axes.text(-0.01, 0.5, "Latitude, [Deg]", size = 12, va = "bottom", ha = "center",
#               rotation = "vertical", rotation_mode = "anchor", transform = axes.transAxes)
#
#     axes.text(0.5, -0.05, "Longitude, [Deg]", size = 12, va = "bottom", ha = "center",
#               rotation = "horizontal", rotation_mode = "anchor", transform = axes.transAxes)
#
#
#     # Add nodes
#     if membership is not None:
#         # Add flights
#         for vertex in graph.vs():
#             print(membership[vertex.index])
#             for edge in graph.es:
#                 # Coordinates
#                 origin = coordinates[edge.tuple[0]]
#                 destination = coordinates[edge.tuple[1]]
#
#                 # Convert to x and y datasets
#                 latitudes = (origin[0], destination[0])
#                 longitudes = (origin[1], destination[1])
#                 colors = ['Tomato','Orange', 'DodgerBlue', 'MediumSeaGreen', 'SlateBlue', "Violet", "#FF3399", "#9CCC65", "#00838F", "#795548"]
#
#                 # Plot
#                 plt.plot(longitudes, latitudes, c=colors[membership[vertex.index]], lw=line_width,
#                          ms=marker_size, ls="-", marker=".", transform=TRANSFORM)
#
#     # Display map
#     plt.show()


if __name__ == "__main__":
    """"Runtime"""
    start_time = time.time()

    community_timeline = []
    community_strength = []

    """"Specifying the filename and location"""
    years = ['2019', '2020']
    months = ['01','02','03','04','05','06','07','08','09','10','11','12'] #'02','03','04','05','06','07','08','09','10','11','12'
    for i in range(len(years)):
        for j in range(len(months)):

            filename = f"EU_flights_{years[i]}_{months[j]}"
            print(f"EU_flights_{years[i]}_{months[j]}")
            path = f'C:\\Users\\phili\\PycharmProjects\\Test-Analysis-Simulation\\{years[i]}_Filtered\\{filename}.csv'

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

            community_timeline.append(clusters)

            membership = clusters.membership
            graph, visual_style = plot(g, filename, membership)
            coords = get_coordinates(ASSET_DIR + AIRPORT_DIR)
            # display_map(graph, coords, membership)


    # def intersection(lst1, lst2):
    #     lst3 = [value for value in lst1 if value in lst2]
    #     return lst3
    # 
    # for i in range(len(years)*len(months)):
    #     best_intersection_list = []
    #     percentage_equal = []
    #     for j in range(len(community_timeline[i])):
    #         list1 = community_timeline[i][j]
    #         print('list1',list1)
    #         intersectionlist = []
    #         intersectionlistindex = []
    # 
    #         try:
    #             for k in range(len(community_timeline[i+1])):
    #                 list2 = community_timeline[i+1][k]
    #                 print('list2',list2)
    #                 inter = intersection(list1,list2)
    #                 intersectionlist.append(inter)
    #                 intersectionlistindex.append(len(inter))
    #             max_interlistindex = max(intersectionlistindex)
    #             print(max_interlistindex)
    #             index_max_interlistindex = intersectionlistindex.index(max_interlistindex)
    #             print('index',index_max_interlistindex)
    #             best_intersection_list.append(intersectionlist[index_max_interlistindex])
    #             print('bestinter', intersectionlist[index_max_interlistindex])
    # 
    #         except:
    #             percentage_equal.append(0)
    # 
    # print(best_intersection_list)



    """"Runtime"""
    print(time.time() - start_time)

#https://www.geeksforgeeks.org/python-intersection-two-lists/

# source of code which helped with visualisation
# https://stackoverflow.com/questions/23184306/draw-network-and-grouped-vertices-of-the-same-community-or-partition
