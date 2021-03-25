"""
This script calculates the centrality measures
and associated parameters.
"""


# ---------- Imports ---------- #
from data_visualization import create_graph


# ---------- Setup ---------- #
GIT_DIR = __file__[0:-20]
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020  = GIT_DIR + "2020_Filtered/"
FLIGHT_DIR = "EU_flights_2020_01.csv"
N = 10


# ---------- Function Definitions ---------- #
def get_closeness(graph):
    """
    This function determines the closeness centrality
    of each node in the graph. It also determines the
    average, weighted average, and the N nodes with
    highest betweenesses.

    Arguments:
        graph (Graph): Graph of the network

    Returns:
        avg_closeness (float): Average closeness of the nodes in the network
        w_avg_closeness (float): Average closeness weighted by node strength
        nodes (List): List of all nodes and closenesses
        top_nodes (List): List of top N nodes ranked by closeness
    """

    # Determine closeness for each node
    closeness = graph.vs.closeness(weights=None)

    # Determine average closeness
    avg_closeness = sum(closeness)/len(closeness)

    # Detemine weighted average closeness
    numerator = 0
    denominator = 0

    for i in range(len(closeness)):
        # Node degree
        degree = graph.degree(graph.vs[i])

        # Update numerator and denominator
        numerator += degree*closeness[i]
        denominator += degree

    w_avg_closeness = numerator/denominator

    # Determine top N nodes
    nodes = []
    for i in range(len(closeness)):
        node = (graph.vs["name"][i], closeness[i])
        nodes.append(node)

    top_nodes = sorted(nodes, key = lambda node: node[1], reverse = True)[0:N]

    return avg_closeness, w_avg_closeness, nodes, top_nodes

# ---------- Main Program ---------- #

# Get graph
graph = create_graph(DIR_2020 + FLIGHT_DIR)

# Determine closeness parameters
closeness = get_closeness(graph)

avg_closeness = closeness[0]
w_avg_closeness = closeness[1]
top_nodes = closeness[3]

print(avg_closeness)
print(w_avg_closeness)
print(top_nodes)

