"""
This script calculates the centrality measures
and associated parameters.
"""


# ---------- Imports ---------- #
from data_visualization import create_graph


# ---------- Setup ---------- #
TEST_DIR = __file__[0:-20] + "2020_Filtered/EU_flights_2020_01.csv"


# ---------- Function Definitions ---------- #
def get_closeness(graph, **args):
    """
    This function determines the closeness centrality
    of each node in the graph. It also determines the
    average, weighted average, and the N nodes with
    highest betweenesses.

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        avg_closeness (float): Average closeness of the nodes in the network
        w_avg_closeness (float): Average closeness weighted by node strength
        nodes (List): List of closenesses of all the nodes
        top_nodes (List): List of top N nodes ranked by closeness
    """

    # Decode arguments
    n_top = args.get("n_top", 10)
    mode = args.get("mode", "all")
    weights = args.get("weights", False)
    normalized = args.get("normalized", True)

    # Determine closeness for each node
    if weights:
        closeness = graph.vs.closeness(mode = mode, weights = graph.es["weight"], normalized = normalized)
    else:
        closeness = graph.vs.closeness(mode = mode, weights = None, normalized = normalized)

    # Detemine weighted average closeness
    numerator = 0
    denominator = 0
    numerator_w = 0
    denominator_w = 0

    for i in range(len(graph.vs)):
        degree = graph.degree(graph.vs[i], mode = mode)
        if degree != 0:
            # Unweighted parameters
            numerator += closeness[i]
            denominator += 1

            # Weighted parameters
            numerator_w += degree*closeness[i]
            denominator_w += degree

    avg_closeness = numerator / denominator
    w_avg_closeness = numerator_w / denominator_w

    # Determine top N nodes
    nodes = []
    for i in range(len(closeness)):
        node = (graph.vs["name"][i], closeness[i])
        nodes.append(node)

    top_nodes = sorted(nodes, key = lambda node: node[1], reverse = True)[0:n_top]

    return avg_closeness, w_avg_closeness, nodes, top_nodes


def get_clustering(graph, **args):
    """
    This function determines the clustering coefficient
    of each node in the graph. It also determines the
    average, weighted average, and the N nodes with
    highest betweenesses.

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        avg_clustering (float): Average clustering coefficient of the nodes in the network
        w_avg_clustering (float): Average clustering coefficient weighted by node strength
        nodes (List): List of clustering coefficients of all the nodes
        top_nodes (List): List of top N nodes ranked by clustering coefficients
    """

    # Decode arguments
    n_top = args.get("n_top", 10)

    # Determine clustering coefficients for each node

    graph.to_undirected()
    #TODO: Weights
    clustering = graph.transitivity_local_undirected()

    # Detemine weighted average clustering coefficients
    numerator = 0
    denominator = 0
    numerator_w = 0
    denominator_w = 0

    for i in range(len(graph.vs)):
        degree = graph.degree(graph.vs[i])
        if degree != 1:
            # Unweighted parameters
            numerator += clustering[i]
            denominator += 1

            # Weighted parameters
            numerator_w += degree*clustering[i]
            denominator_w += degree

    avg_clustering = numerator / denominator
    w_avg_clustering = numerator_w / denominator_w

    # Determine top N nodes
    nodes = []
    for i in range(len(clustering)):
        node = (graph.vs["name"][i], clustering[i])
        nodes.append(node)

    top_nodes = sorted(nodes, key = lambda node: node[1], reverse = True)[0:n_top]

    return avg_clustering, w_avg_clustering, nodes, top_nodes


def get_giant_component(graph, **args):
    """
    This function determines the giant component
    of the graph, as well as its size.

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        giant (Graph): Giant component of the graph
        len(giant) (int): Size of the giant component of the graph
    """

    # Determine giant component
    giant = graph.components().giant().vs["name"]

    return giant, len(giant)


# ---------- Main Program ---------- #
if __name__ == "__main__":

    # Get graph
    graph_flights = create_graph(TEST_DIR)

    # Determine parameters
    closeness_flights = get_closeness(graph_flights, mode = "in", weights = True)
    clustering_flights = get_clustering(graph_flights)

    # Print results
    print("Average Closeness: " + str(closeness_flights[0]))
    print("Weighted Average Closeness: " + str(closeness_flights[1]))
    print("Top N nodes: ")
    print(closeness_flights[3])
    print()

    print("Average Clustering Coefficient: " + str(clustering_flights[0]))
    print("Weighted Average Clustering Coefficient: " + str(clustering_flights[1]))
    print("Top N nodes: ")
    print(clustering_flights[3])
    print()