"""
This script performs network restoration. The graphs of the networks for 04/2019
and 04/2020 are used. By restoring the weight of each edge in a predefined set to
its previous value, the effect on the average centrality measure desired is 
determined. This value is then normalized using the ideal change in the average
and divided by the total number of flights required, to obtain a restoration
"efficiency" value. The routes where network restoration is most efficient are
then ranked such that they can be compared for different centrality measures. 
"""


# ---------- Imports ---------- #
from data_visualization import create_graph
import numpy as np
import matplotlib.pyplot as plt
import itertools
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
airport_list = []
for airport in airport_csv:
    airport_list.append(airport[1])

del airport_list[0]              # Remove legend
airportSet = set(airport_list)   # Convert to Set

TARGETS = airport_list

# TARGETS = ["EGLL", "LFPG", "EDDF", "EHAM", "LEMD", "EDDM", "LIRF", "EGKK", "LEBL", "UUDD",
#               "UUEE", "LFPO", "LSZH", "EKCH", "ENGM", "LEPA", "LOWW", "EDLL", "EGCC", "ESSA"]

# ---------- Function Definitions ---------- #
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

def betweenness(graph):
    betweeness = graph.vs.betweenness(weights = graph.es["weight"])

    # Detemine average closeness
    num, den = 0, 0
    for i in range(len(graph.vs)):
        num += betweeness[i]
        den += 1
        
    return num/den

def weighted_degree(graph):
    # Detemine average closeness
    num = 0
    for vertex in graph.vs:
        num += sum(graph.es.select(_incident = [vertex])["weight"])

    return num/len(graph.vs)


# ---------- Main Program ---------- #
# Start time
start_time = time.time()

# Determine graphs
graph_2019 = create_graph(FLIGHT_DIR_2019)
graph_2020 = create_graph(FLIGHT_DIR_2020)

# Get target & starting measures
measure_2019 = weighted_degree(graph_2019)
measure_2020 = weighted_degree(graph_2020)

# Get List of ICAO code pairs
icao_pairs = itertools.combinations(TARGETS, 2)

# Prepare results
results = np.zeros((len(TARGETS), len(TARGETS)))
top = []

# Iterate through edges
for icao_pair in icao_pairs:
    # Get ids of both nodes
    index_pair_2019 = graph_2019.vs.select(name_in = icao_pair).indices
    index_pair_2020 = graph_2020.vs.select(name_in = icao_pair).indices #TODO: ORDER MIGHT COME OUT REVERSED

    try:
        # Get edges for 2019
        edge_2019_0 = graph_2019.es.select(_from = index_pair_2019[0], _to = index_pair_2019[1])[0]
        edge_2019_1 = graph_2019.es.select(_from = index_pair_2019[1], _to = index_pair_2019[0])[0]

        # Get edges for 2020
        edge_2020_0 =  graph_2020.es.select(_from = index_pair_2020[0], _to = index_pair_2020[1])[0]
        edge_2020_1 =  graph_2020.es.select(_from = index_pair_2020[1], _to = index_pair_2020[0])[0]

    except IndexError:
        continue

    # Backup 2020 weights
    weight_2020_0 = edge_2020_0["weight"]
    weight_2020_1 = edge_2020_1["weight"]

    # Determine virtual weights (AKA 2019 weights)
    weight_virtual_0 = edge_2019_0["weight"]
    weight_virtual_1 = edge_2019_1["weight"]

    # Update graph
    edge_2020_0["weight"] = weight_virtual_0
    edge_2020_1["weight"] = weight_virtual_1

    # Get updated measure
    measure_virtual = weighted_degree(graph_2020)

    # Get required change in flights
    delta_flights = (weight_virtual_0 + weight_virtual_1) - (weight_2020_0 + weight_2020_1)

    # Normalize & Scale average node weight
    measure_normalized = (measure_virtual - measure_2020) / (measure_2019 - measure_2020)
    measure_specific = measure_normalized #/ delta_flights #TODO: FIX

    # Set edge weights back to their original values
    edge_2020_0["weight"] = weight_2020_0
    edge_2020_1["weight"] = weight_2020_1

    # Add datapoint
    results[TARGETS.index(icao_pair[0]), TARGETS.index(icao_pair[1])] = measure_specific
    top.append((icao_pair[0], icao_pair[1], measure_specific))

# Show elapsed time
print("Process time: " + str(time.time() - start_time) + " [s]\n")

# Show rankings
print("Top 100 routes:")
for route in sorted(top, key=lambda x: x[2], reverse=True)[:]:
    print(route)

# Plot results
plt.matshow(np.ma.masked_equal(results, 0.0))

# Configure plot
plt.title("Restoration Efficiency")
plt.xticks(list(range(len(TARGETS))), TARGETS, rotation = 45)
plt.yticks(list(range(len(TARGETS))), TARGETS, rotation = 45)
plt.axis("scaled")
plt.colorbar()

# Show plot
plt.show()