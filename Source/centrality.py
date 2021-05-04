""" This script determines the centrality measures """


# ---------- Imports ---------- #
from data_visualization import create_graph


# ---------- Setup ---------- #
TEST_DIR = __file__[0:-20] + "2020_Filtered/EU_flights_2020_01.csv"


# ---------- Function Definitions ---------- #
def get_assortativity(graph, airports, **args):
    """
    This function determines the assortativity of the graph

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        avg (float): Graph assortatibity
    """

    # Decode arguments
    directed = args.get("directed", True)

    # Determine assortativity
    assorativity = graph.assortativity_degree(directed = directed)

    return assorativity, None

def get_betweenness(graph, airports, **args):
    """
    This function determines the betweenness centrality of each node in
    the graph. It also determines the average of those betweennesses.

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        num/den (float): Average betweenness of the nodes in the network
        nodes (List): Betweennesses
    """

    # Decode arguments
    directed = args.get("directed", True)
    weighted = args.get("weighted", True)

    # Determine closeness for each node
    if weighted:
        betweeness = graph.vs.betweenness(directed = directed, weights = graph.es["weight"])
    else:
        betweeness = graph.vs.betweenness(directed = directed, weights = None)

    # Detemine average closeness
    num, den = 0, 0
    for i in range(len(graph.vs)):
        num += betweeness[i]
        den += 1

    # Create list for the selected airports
    nodes = []
    for i in range(len(graph.vs)):
        if graph.vs["name"][i] in airports:
            nodes.append(betweeness[i])

    return num/den, nodes


def get_closeness(graph, airports, **args):
    """
    This function determines the closeness centrality of each node in
    the graph. It also determines the average of those closenesses.

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        num/den (float): Average closeness of the nodes in the network
        nodes (List): Closenesses
    """

    # Decode arguments
    mode = args.get("mode", "all")
    weighted = args.get("weighted", True)
    normalized = args.get("normalized", True)

    # Determine closeness for each node
    if weighted:
        closeness = graph.vs.closeness(mode = mode, weights = graph.es["weight"], normalized = normalized)
    else:
        closeness = graph.vs.closeness(mode = mode, weights = None, normalized = normalized)

    # Detemine average closeness
    num, den = 0, 0
    for i in range(len(graph.vs)):
        if graph.degree(graph.vs[i], mode = mode) != 0:
            num += closeness[i]
            den += 1

    # Create list for the selected airports
    nodes = []
    for i in range(len(graph.vs)):
        if graph.vs["name"][i] in airports:
            nodes.append(closeness[i])

    return num/den, nodes


def get_clustering(graph, airports, **args):
    """
    This function determines the clustering coefficient of each node in
    the graph. It also determines the average of those coefficients.

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        num/den (float): Average clustering coefficient of the nodes in the network
        nodes (List): List of clustering coefficients of all the nodes
    """

    # Determine clustering coefficients for each node
    graph.to_undirected()
    clustering = graph.transitivity_local_undirected()


    # Detemine average clustering coefficients
    num, den = 0, 0
    for i in range(len(graph.vs)):
        if graph.degree(graph.vs[i]) > 1:
            num += clustering[i]
            den += 1

    # Create list for the selected airports
    nodes = []
    for i in range(len(graph.vs)):
        if graph.vs["name"][i] in airports:
            nodes.append(clustering[i])

    return num/den, nodes

def get_degree(graph, airports, **args):
    """
    This function determines the degree of each node in the
    graph. It also determines the average of those closenesses.

    Arguments:
        graph (Graph): Graph of the network
        **args (Dict): Optional arguments

    Returns:
        avg (float): Average degree of the nodes in the network
        nodes (List): Degrees
    """

    # Decode arguments
    mode = args.get("mode", "all")

    # Determine degree for each node
    degree = graph.vs.degree(mode = mode)

    # Detemine average degree
    avg = sum(degree)/len(degree)

    # Create list for the selected airports
    nodes = []
    for i in range(len(graph.vs)):
        if graph.vs["name"][i] in airports:
            nodes.append(degree[i])

    return avg, nodes


# ---------- Main Program ---------- #
if __name__ == "__main__":

    # Get graph
    graph_flights = create_graph(TEST_DIR)

    # Determine parameters
    assortatvity_flights = get_assortativity(graph_flights, [])
    betweenness_flights = get_betweenness(graph_flights, [])
    closeness_flights = get_closeness(graph_flights, [])
    degree_flights = get_degree(graph_flights, [])

    # Do this last as it messes up the graph
    clustering_flights = get_clustering(graph_flights, [])

    # Print results
    print("Average Assortativity: " + str(assortatvity_flights[0]))
    print("Average Betweenness: " + str(betweenness_flights[0]))
    print("Average Closeness: " + str(closeness_flights[0]))
    print("Average Clustering Coefficient: " + str(clustering_flights[0]))
    print("Average Degree: " + str(degree_flights[0]))