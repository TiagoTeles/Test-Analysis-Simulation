"""
This script calculates the size of the giant component in two ways,
based on the adjacency matrices.

"""

# ---------- Imports ---------- #
import time
import csv
from adjacency import get_matrices



## ---------- Function Definitions ---------- ##
def get_giantcomponent1(flightlist):
    """
        Constructs the giant component and size of this giant component
        from the adjacency matrix from a specific network, based on the
        MUTUAL connectivity between airports

        Arguments:
            flightlist (List): List of flights to be considered

        Returns:
            giant_component (list): list of the nodes in the giant component
            weight_matrix (ndarray): Weight matrix
            airports (list): Sorted airport list
        """
    adjacency_matrix, airports = get_matrices(flightlist)
    giant_component = []


    for i in range(len(airports)):
        for j in range(len(airports)):
            if (adjacency_matrix[i][j] == 1) and (adjacency_matrix[j][i] == 1):
                giant_component.append(airports[i])
                giant_component.append(airports[j])
            else:
                continue

    giant_component = set(giant_component)
    size = len(giant_component)

    return giant_component, size


def get_giantcomponent2(flightlist):
    """
           Constructs the giant component and size of this giant component
           from the adjacency matrix from a specific network, based on the
           SINGLE connectivity between airports

           Arguments:
               flightlist (List): List of flights to be considered

           Returns:
               giant_component (list): list of the nodes in the giant component
               weight_matrix (ndarray): Weight matrix
               airports (list): Sorted airport list
           """
    adjacency_matrix, airports = get_matrices(flightlist)

    giant_component = []

    for i in range(len(airports)):
        for j in range(len(airports)):
            if (adjacency_matrix[i][j] == 1) or (adjacency_matrix[j][i] == 1):
                giant_component.append(airports[i])
                giant_component.append(airports[j])
            else:
                continue

    giant_component = set(giant_component)
    size = len(giant_component)

    return giant_component, size


## ---------- Main Program ---------- ##
if __name__ == "__main__":
    # Define directories
    GIT_DIR = __file__[0:-25]
    ASSET_DIR = GIT_DIR + "Assets/"
    DIR_2019 = GIT_DIR + "2019_Filtered/"
    DIR_2020  = GIT_DIR + "2019_Filtered/"

    # Define input file name
    FLIGHT_DIR = "EU_flights_2019_06.csv"   # .CSV containing list of filtered flights

    # Open files
    flight_file = open(DIR_2020 + FLIGHT_DIR, encoding="utf8")

    # Read files
    flight_csv = csv.reader(flight_file)

    # Convert flight database from .CSV to List
    flight_list = []
    for flight in flight_csv:
        flight_list.append(flight)

    del flight_list[0] # Remove legend


    # Calculate Giant components
    start_time = time.time()

    # Print runtime
    print("Runtime:", round(time.time() - start_time, 1), "s")