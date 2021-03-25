"""
This script imports the relevant data from .CSV file, converts it to lists,
and uses the weight matrix to create calculate the node strengths.

The Flights.CSV file has the following structure:
Callsign, Origin, Destination


"""

# ----- Imports ----- #

import numpy as np
import time
import csv

from adjacency import get_matrices



# ----- Function Definition ----- #
def get_Node_strength(weightMatrix):
    # ----- Defining the function to find the node strengths ----- #
    """ Constructs a list with node strengths from the data provided.
        The index of a specific entry of the node strength list corresponds to the
        same entry with that index in the node (airport) list.

    Arguments:
        weightMatrix {n-n matrix formed by np.arrays} -- Weight matrix of network
        
    Returns:
        list -- node_strength
    """
    transposed = weightMatrix.transpose()
    
    in_node_strength = []
    out_node_strength = []
    
    for row in weightMatrix:
        in_node_strength.append(sum(row))

    for row in transposed:
        out_node_strength.append(sum(row))


    total_node_strength = []
    
    for i in range(len(in_node_strength)):
        total_node_strength.append(in_node_strength[i] + out_node_strength[i])


    return in_node_strength, out_node_strength, total_node_strength


def average_node_strenght(node_strength):
    # ----- Defining the function to find the average node strength ----- #
    """ Constructs a value of average node strength.

    Arguments:
        node_strength {List} -- List with node strengths of nodes

    Returns:
        value -- average_strength
    """

    inclined = 0
    total = 0

    for strength in node_strength:
        inclined = inclined + strength
        total += 1

    average_strength = inclined/total
    return average_strength

## ---------- Main Program ---------- ##
if __name__ == "__main__":

    '''  Function testing '''
    # Define directories
    GITDIR = __file__[0:-32]
    assetDir = GITDIR + "Assets/"
    dir2019 = GITDIR + "2019_Filtered/"
    dir2020  = GITDIR + "2020_Filtered/"

    # Define input file name
    flightFile = "EU_flights_2019_01.csv"   # .CSV containing list of filtered flights

    # Open files
    flightsFile = open(dir2019 + flightFile, encoding="utf8")

    # Read files
    flightsCSV = csv.reader(flightsFile)

    # Convert flight database from .CSV to List
    flightList = []
    for flight in flightsCSV:
       flightList.append(flight)

    del (flightList[0]) # Remove legend


    # Calculate Matrices
    startTime = time.time()
    adjacency, weight, _ = get_matrices(flightList)

    # Use matrices to get the node strengths
    in_strength, out_strength, total_strength = get_Node_strength(weight)
    print('In strength', in_strength, '\n')
    print('Out strength', out_strength, '\n')
    print('Total strength', total_strength, '\n')
