"""

"""


# ---------- Imports ---------- #
from data_visualization import create_graph
import itertools
import igraph as ig
import time


# ---------- Setup --------- #
# Define directories
GIT_DIR = __file__[0:-29]
FLIGHT_DIR_2019 = GIT_DIR + "2019_Filtered/EU_flights_2019_04.csv"
FLIGHT_DIR_2020 = GIT_DIR + "2020_Filtered/EU_flights_2020_04.csv"

# List of airports to try restoration
TARGETS = ["EGLL", "LFPG", "EDDF", "EHAM", "LEMD"]


# ---------- Function Definitions ---------- #


# ---------- Main Program ---------- #
# Start timer
start_time = time.time()

# Determine graphs
graph_2019 = create_graph(FLIGHT_DIR_2019)
graph_2020 = create_graph(FLIGHT_DIR_2020)

# Get icao code pairs
icao_pairs = itertools.combinations(TARGETS, 2)

# Iterate through edges
for pair in icao_pairs:
    vertex_pair = graph_2020.vs.select(name_in = pair)

    for edge in graph_2020.es.select(_within = vertex_pair):
        print(edge)

    print()

print(time.time() - start_time)

# Change in the parameter required to fully restore the network
#delta_desired = func(graph_2020) - func(graph_2019)




## Determine list of edges to be checked (Either top airports or top decrese during the pandemic) (NC2)

## for each edge, make the weight equal to value from 2019
## Calculate difference in parameter for the network and divide by desired change
## Note the effort (Number of flights added) to the edge

## Determine and rank Percentage chage per flight added
