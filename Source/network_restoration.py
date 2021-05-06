"""
This script performs network restoration. The graphs of the networks for 04/2019
and 04/2020 are used. By restoring the weights of the edges connected to each 
individual node, the effect on the average centrality measure desired is 
determined. This value is then normalized using the ideal change in the average
and divided by the total number of flights required, to obtain a restoration
"efficiency" value. The routes where network restoration is most efficient are
then ranked such that they can be compared for different centrality measures. 
"""


# ---------- Imports ---------- #
from data_visualization import create_graph
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

# ---------- Setup --------- #
# Define directories
GIT_DIR = __file__[0:-29]
FLIGHT_DIR_2019 = GIT_DIR + "2019_Filtered/EU_flights_2019_04.csv"
FLIGHT_DIR_2020 = GIT_DIR + "2020_Filtered/EU_flights_2020_04.csv"
AIRPORT_DIR = GIT_DIR + "Assets/Airports.csv"

# List of airports to try restoration
airport_file = open(AIRPORT_DIR, encoding="utf8")
airport_csv = csv.reader(airport_file)

# Convert airport codes from .CSV to List
airports = []
for airport in airport_csv:
    airports.append(airport[1])

# Remove legend
del airports[0]


# ---------- Function Definitions ---------- #
def betweenness(graph):
    # Determine betweenness of each node
    betweeness = graph.vs.betweenness(weights = graph.es["weight"])

    # Detemine average closeness
    num, den = 0, 0
    for i in range(len(graph.vs)):
        num += betweeness[i]
        den += 1
        
    return num/den

def closeness(graph):
    # Determine closeness of each node
    closeness = graph.vs.closeness(weights = graph.es["weight"])

    # Detemine average closeness
    num, den = 0, 0
    for i in range(len(graph.vs)):
        if graph.degree(graph.vs[i]) != 0:
            num += closeness[i]
            den += 1

    return num/den

def weighted_degree(graph):
    # Detemine average closeness
    num = 0
    for vertex in graph.vs:
        num += sum(graph.es.select(_incident = [vertex])["weight"])

    return num/len(graph.vs)


# ---------- Main Program ---------- #
# Start timer
start_time = time.time()

# Determine graphs
graph_2019 = create_graph(FLIGHT_DIR_2019)
graph_2020 = create_graph(FLIGHT_DIR_2020)

# Get target & starting measures
measure_2019 = weighted_degree(graph_2019)
measure_2020 = weighted_degree(graph_2020)

# Store results
efficiency = []

# Iterate through nodes
for icao_main in airports:

    # Initialize variables
    n_flights = 0
    
    # Get vertex ID from ICAO code
    vertex_main_2019 = graph_2019.vs.select(name = icao_main)
    vertex_main_2020 = graph_2020.vs.select(name = icao_main)

    # Get edges connected to main from 2019
    edges_dep_2019 = graph_2019.es.select(_from_in = vertex_main_2019)
    edges_arr_2019 = graph_2019.es.select(_to_in = vertex_main_2019)

    # Get edges connected to main from 2020
    edges_dep_2020 = graph_2020.es.select(_from_in = vertex_main_2020)
    edges_arr_2020 = graph_2020.es.select(_to_in = vertex_main_2020)

    # Get departures from main in 2019
    for edge_2020 in edges_dep_2020:
        icao_sub = graph_2020.vs["name"][edge_2020.target]
        vertex_sub_2019 = graph_2019.vs.select(name = icao_sub)
        edge_2019 = edges_dep_2019.select(_to_in = vertex_sub_2019)

        if len(edge_2019) != 0:
            # Get weights
            weight_2019 = edge_2019["weight"][0]
            weight_2020 = edge_2020["weight"]

            # Update weight
            edge_2020["weight"] = weight_2019

            # Get additional flights
            n_flights += abs(weight_2019 - weight_2020)

    # Get arrivals to main in 2019
    for edge_2020 in edges_dep_2020:
        icao_sub = graph_2020.vs["name"][edge_2020.source]
        vertex_sub_2019 = graph_2019.vs.select(name = icao_sub)
        edge_2019 = edges_arr_2019.select(_from_in = vertex_sub_2019)

        if len(edge_2019) != 0:
            # Get weights
            weight_2019 = edge_2019["weight"][0]
            weight_2020 = edge_2020["weight"]

            # Update weight
            edge_2020["weight"] = weight_2019

            # Get additional flights
            n_flights += abs(weight_2019 - weight_2020)


    # Get updated measure
    measure_virtual = weighted_degree(graph_2020)

    # Normalize & Scale average node weight
    if n_flights != 0:
        measure_normalized = (measure_virtual - measure_2020) / (measure_2019 - measure_2020)
        measure_specific = measure_normalized / n_flights
        efficiency.append((icao_main, measure_specific))

    # Reset graph
    graph_2020 = create_graph(FLIGHT_DIR_2020)

# Show elapsed time
print("Process time: " + str(time.time() - start_time) + " [s]\n")

# Sort result
efficiency.sort(key=lambda x: x[1], reverse=True)

# Select top N
efficiency = efficiency[0:10]

# Plot result
plt.title("Network Restoration")
plt.ylabel("Restoration Efficiency")
plt.bar(*zip(*efficiency))

# Show plot
plt.show()