"""
This script calculates the centrality measures
and associated parameters.
"""


# ---------- Imports ---------- #
from data_visualization import create_graph
from math import isnan


# ---------- Setup ---------- #
GIT_DIR = __file__[0:-20]
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020  = GIT_DIR + "2020_Filtered/"
FLIGHT_DIR = "EU_flights_2020_01.csv"
N = 10


# ---------- Function Definitions ---------- #
def get_closeness_in(graph):
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
        top_nodes (List): List of top N nodes ranked by closeness
    """

    # Determine closeness for each node
    closeness = graph.vs.closeness(mode = "in")

    # Detemine weighted average closeness
    numerator = 0
    denominator = 0
    numerator_w = 0
    denominator_w = 0

    for i in range(len(closeness)):
        if not isnan(closeness[i]):
            # Node degree
            degree = graph.degree(graph.vs[i])

            # Update unweighted numerator and denominator
            numerator += closeness[i]
            denominator += 1

            # Update weighted numerator and denominator
            numerator_w += degree*closeness[i]
            denominator_w += degree

    avg_closeness = numerator / denominator
    w_avg_closeness = numerator_w/denominator_w

    # Determine top N nodes
    nodes = []
    for i in range(len(closeness)):
        node = (graph.vs["name"][i], closeness[i])
        nodes.append(node)

    top_nodes = sorted(nodes, key = lambda node: node[1], reverse = True)[0:N]

    return avg_closeness, w_avg_closeness, top_nodes


def get_closeness_out(graph):
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
        top_nodes (List): List of top N nodes ranked by closeness
    """

    # Determine closeness for each node
    closeness = graph.vs.closeness(mode = "out")

    # Detemine weighted average closeness
    numerator = 0
    denominator = 0
    numerator_w = 0
    denominator_w = 0

    for i in range(len(closeness)):
        if not isnan(closeness[i]):
            # Node degree
            degree = graph.degree(graph.vs[i])

            # Update unweighted numerator and denominator
            numerator += closeness[i]
            denominator += 1

            # Update weighted numerator and denominator
            numerator_w += degree*closeness[i]
            denominator_w += degree

    avg_closeness = numerator / denominator
    w_avg_closeness = numerator_w/denominator_w

    # Determine top N nodes
    nodes = []
    for i in range(len(closeness)):
        node = (graph.vs["name"][i], closeness[i])
        nodes.append(node)

    top_nodes = sorted(nodes, key = lambda node: node[1], reverse = True)[0:N]

    return avg_closeness, w_avg_closeness, top_nodes


def get_giant_component(graph):
    """
    This function determines the giant component
    of the graph, as well as its size.

    Arguments:
        graph (Graph): Graph of the network

    Returns:
        len(giant) (int): Size of the giant component of the graph
        giant (Graph): Giant component of the graph
    """

    # Determine giant component
    giant = graph.components().giant().vs["name"]

    return len(giant), giant


# ---------- Main Program ---------- #
if __name__ == "__main__":
    # Get graph
    graph = create_graph(DIR_2020 + FLIGHT_DIR)

    # Determine closeness parameters
    closeness = get_closeness_in(graph)

    avg_closeness = closeness[0]
    w_avg_closeness = closeness[1]
    top_nodes = closeness[2]

    print(avg_closeness)
    print(w_avg_closeness)
    print(top_nodes)