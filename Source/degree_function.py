"""
This script determines all the in-degree, out-degree, and total degree
distributions of a network. It also determines the number of distinct
edges each node is connected to.
"""

# ---------- Imports ---------- #
import numpy as np

# ---------- Function Definitions ---------- #
def node_degree(weight_matrix):
    """
    Determines the degrees of the network. The row index
    corresponds to the index of the origin airport, the
    column index corresponds to the destination airport.
    It also determines the number of distinct edges each
    node is connected to.

    Arguments:
        weight_matrix (nd.array): Weight matrix of the network

    Returns:
        out_degree_list (List): In-Degree distribution of the network
        in_degree_list (List): Out-Degree distribution of the network
        diff_links_list (List): Number of distinct edges connected to each node of th network
        degree_list (List): Total degree distribuition of the network
    """

    # Determine the degrees
    in_degree_list = np.count_nonzero(weight_matrix, axis=0)    # Constant column index
    out_degree_list = np.count_nonzero(weight_matrix, axis=1)   # Constant row index
    degree_list = in_degree_list + out_degree_list

    # Determine the number of different edges connected to a node
    diff_links_list = []
    weight_matrix_t = np.transpose(weight_matrix)

    for i in range(len(weight_matrix)):
        # Row and column of airport i
        row = weight_matrix[i]
        column = weight_matrix_t[i]

        # Backup ckeck, should always be true
        row[i] = 0
        column[i] = 0

        # Determine number of different edges
        diff_links_list.append(np.count_nonzero(row + column))

    return out_degree_list, in_degree_list, diff_links_list, degree_list

def average_degree(degree_list):
    """ 
    Calculates the average degree of a network.

    Arguments:
        degree_list (List): List of node degrees

    Returns:
        (Float): Average degree of the network
    """

    return sum(degree_list)/len(degree_list)

## ---------- Main Program ---------- ##
if __name__ == "__main__":
    # Used for testing the function node_degree()
    test_array = np.array([
        [0,3,10,0,5,0],
        [3,0,0 ,0,5,6],
        [0,0,0 ,0,0,0],
        [1,3,10,0,5,3],
        [0,3,10,5,0,0],
        [0,0,0 ,0,5,0]
        ])

    # Determine degrees
    out_degree_list, in_degree_list, diff_links_list, degree_list = node_degree(test_array)

    # Determine average degree
    avg_degree = average_degree(degree_list)

    # Print results
    print("In-Degree:", in_degree_list)
    print("Out-Degree:", out_degree_list)
    print("Total Degree:", degree_list)
    print("Distinct edges:", diff_links_list)
    print("Average degree:", avg_degree)
