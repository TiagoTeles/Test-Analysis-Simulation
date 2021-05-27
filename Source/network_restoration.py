"""
This script performs network restoration. The graphs of the networks for 04/2019
and 04/2020 are used. By restoring the weights of the edges connected to each
individual node, the effect on the average centrality measure desired is
determined. This value is then normalized using the ideal change in the average
to obtain a restoration "efficiency" value. The routes where network restoration
is most efficient are then ranked such that they can be compared for different
centrality measures.
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
FLIGHT_DIR_2019 = GIT_DIR + "Combined_2019_new/Combined_2019_04_b.csv"
FLIGHT_DIR_2020 = GIT_DIR + "Combined_2020_new/Combined_2020_04_b.csv"
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
    weights = [1/w for w in graph.es["weight"]]
    betweeness = graph.vs.betweenness(weights=weights)

    # Normalize
    N = len(graph.vs)
    betweeness = [i/((N-1)*(N-2)) for i in betweeness]

    return sum(betweeness)/len(betweeness)

def show(efficiency, N):
    # Fromat the plot
    plt.rcParams['font.size'] = '13'
    plt.rcParams['legend.framealpha'] = '0.4'
    plt.rcParams['figure.figsize'] = 9.3, 6.5

    # Plot result
    plt.ylabel("Restoration Efficiency", fontsize=16)
    plt.tight_layout()
    plt.bar(*zip(*(efficiency[0:N])))

    # Show plot
    plt.show()

def show_cumulative(efficiency):
    # Fromat the plot
    plt.rcParams['font.size'] = '13'
    plt.rcParams['legend.framealpha'] = '0.4'
    plt.rcParams['figure.figsize'] = 9.3, 6.5

    # Plot result
    plt.ylabel("Restoration Efficiency", fontsize=16)
    plt.xlabel("Number of airports restored", fontsize=16)
    plt.ylim(0.0, 1.0)
    plt.tight_layout()
    plt.bar(*zip(*efficiency))

    # Show plot
    plt.show()


def restore():
    # Determine graphs
    graph_2019 = create_graph(FLIGHT_DIR_2019)
    graph_2020 = create_graph(FLIGHT_DIR_2020)

    # Get target & starting measures
    measure_2019 = betweenness(graph_2019)
    measure_2020 = betweenness(graph_2020)

    # Store results
    efficiency = []

    # Iterate through nodes
    for icao_main in airports:

        # Initialize variables
        n_flights = 0

        # Get vertex ID from ICAO code
        vertex_main_2019 = graph_2019.vs.select(name=icao_main)
        vertex_main_2020 = graph_2020.vs.select(name=icao_main)

        # Get edges connected to main from 2019
        edges_dep_2019 = graph_2019.es.select(_from_in=vertex_main_2019)
        edges_arr_2019 = graph_2019.es.select(_to_in=vertex_main_2019)

        # Get edges connected to main from 2020
        edges_dep_2020 = graph_2020.es.select(_from_in=vertex_main_2020)
        edges_arr_2020 = graph_2020.es.select(_to_in=vertex_main_2020)

        # Get departures from main in 2019
        for edge_2020 in edges_dep_2020:
            icao_sub = graph_2020.vs["name"][edge_2020.target]
            vertex_sub_2019 = graph_2019.vs.select(name=icao_sub)
            edge_2019 = edges_dep_2019.select(_to_in=vertex_sub_2019)

            if len(edge_2019) != 0:
                # Get weights
                weight_2019 = edge_2019["weight"][0]
                weight_2020 = edge_2020["weight"]

                # Update weight
                edge_2020["weight"] = weight_2019

                # Get additional flights
                n_flights += abs(weight_2019 - weight_2020)

        # Get arrivals to main in 2019
        for edge_2020 in edges_arr_2020:
            icao_sub = graph_2020.vs["name"][edge_2020.source]
            vertex_sub_2019 = graph_2019.vs.select(name=icao_sub)
            edge_2019 = edges_arr_2019.select(_from_in=vertex_sub_2019)

            if len(edge_2019) != 0:
                # Get weights
                weight_2019 = edge_2019["weight"][0]
                weight_2020 = edge_2020["weight"]

                # Update weight
                edge_2020["weight"] = weight_2019

        # Get updated measure
        measure_virtual = betweenness(graph_2020)

        # Normalize & Scale average node weight
        if n_flights != 0:
            measure_normalized = (measure_virtual - measure_2020) / (measure_2019 - measure_2020)
            efficiency.append((icao_main, measure_normalized))

        # Reset graph
        graph_2020 = create_graph(FLIGHT_DIR_2020)

    # Sort result
    efficiency.sort(key=lambda x: x[1], reverse=True)

    return efficiency


def restore_cumulative(efficiency, N):
    # Determine graphs
    graph_2019 = create_graph(FLIGHT_DIR_2019)
    graph_2020 = create_graph(FLIGHT_DIR_2020)

    # Get target & starting measures
    measure_2019 = betweenness(graph_2019)
    measure_2020 = betweenness(graph_2020)

    # Store results
    efficiency_cumulative = []

    # Iterate through nodes
    for i in range(N):

        # Initialize variables
        n_flights = 0
        icao_main = list(zip(*efficiency))[0][0:i+1]

        # Get vertex ID from ICAO code
        vertex_main_2019 = graph_2019.vs.select(name_in=icao_main)
        vertex_main_2020 = graph_2020.vs.select(name_in=icao_main)

        # Get edges connected to main from 2019
        edges_dep_2019 = graph_2019.es.select(_from_in=vertex_main_2019)
        edges_arr_2019 = graph_2019.es.select(_to_in=vertex_main_2019)

        # Get edges connected to main from 2020
        edges_dep_2020 = graph_2020.es.select(_from_in=vertex_main_2020)
        edges_arr_2020 = graph_2020.es.select(_to_in=vertex_main_2020)

        # Get departures from main in 2019
        for edge_2020 in edges_dep_2020:
            icao_sub = graph_2020.vs["name"][edge_2020.target]
            vertex_sub_2019 = graph_2019.vs.select(name=icao_sub)
            edge_2019 = edges_dep_2019.select(_to_in=vertex_sub_2019)

            if len(edge_2019) != 0:
                # Get weights
                weight_2019 = edge_2019["weight"][0]
                weight_2020 = edge_2020["weight"]

                # Update weight
                edge_2020["weight"] = weight_2019

                # Get additional flights
                n_flights += abs(weight_2019 - weight_2020)

        # Get arrivals to main in 2019
        for edge_2020 in edges_arr_2020:
            icao_sub = graph_2020.vs["name"][edge_2020.source]
            vertex_sub_2019 = graph_2019.vs.select(name=icao_sub)
            edge_2019 = edges_arr_2019.select(_from_in=vertex_sub_2019)

            if len(edge_2019) != 0:
                # Get weights
                weight_2019 = edge_2019["weight"][0]
                weight_2020 = edge_2020["weight"]

                # Update weight
                edge_2020["weight"] = weight_2019

        # Get updated measure
        measure_virtual = betweenness(graph_2020)

        # Normalize & Scale average node weight
        if n_flights != 0:
            measure_normalized = (measure_virtual - measure_2020) / (measure_2019 - measure_2020)
            efficiency_cumulative.append((str(i+1), measure_normalized))

        # Reset graph
        graph_2020 = create_graph(FLIGHT_DIR_2020)

    return efficiency_cumulative

# ---------- Main Program ---------- #
if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    # Run algorithm & show results
    efficiency = restore()
    show(efficiency, 10)

    efficiency_cumulative = restore_cumulative(efficiency, 10)
    print(efficiency_cumulative)
    show_cumulative(efficiency_cumulative)

    # Show elapsed time
    print("Process time: " + str(time.time() - start_time) + " [s]\n")
