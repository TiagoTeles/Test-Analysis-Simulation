"""
This script imports the relevant data from .CSV files, converts it to lists,
and creates directed adjacency and weight matrices from those lists.

The Flights.CSV file has the following structure:
Callsign, Origin, Destination, Date

The Airports.CSV file has the following structure:
Size, ICAO Code, IATA Code, Name, Latitude, Longitude, Country
"""

# ---------- Imports ---------- #
import time
import csv
import numpy as np


## ---------- Function Definitions ---------- ##
def get_matrices(flight_list):
    """
    Constructs directed adjacency and weight matrices from the data provided.
    The row index corresponds to index of the origin airport, the column index
    corresponds to the destination airport.

    Arguments:
        flight_list (List): List of flights to be considered

    Returns:
        adjacency_matrix (ndarray): Adjacency matrix
        weight_matrix (ndarray): Weight matrix
        airports (list): Sorted airport list
    """

    # Get list of unique airports
    used_airports = []
    for flight in flight_list:
        used_airports.append(flight[1])
        used_airports.append(flight[2])

    airports = list(set(used_airports)) # Remove duplicates
    airports.sort() # Order alphabetically

    # Create empty matrices
    n = len(airports)
    adjacency_matrix = np.zeros((n, n), int)
    weight_matrix = np.zeros((n, n), int)

    # Iterate over flights
    for flight in flight_list:
        # Determine indices
        origin_index = airports.index(str(flight[1]))
        destination_index = airports.index(str(flight[2]))

        # Update matrices
        adjacency_matrix[origin_index][destination_index] = 1
        weight_matrix[origin_index][destination_index] += 1

    return adjacency_matrix, weight_matrix, airports


## ---------- Main Program ---------- ##
if __name__ == "__main__":
    # Define directories
    GIT_DIR = __file__[0:-19]
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


    # Calculate Matrices
    start_time = time.time()
    adjacency, weight, airports = get_matrices(flight_list)

    # Print matricies
    # print("\n")
    # print(adjacency)
    # print("\n")
    # print(weight)
    # print("\n")
    print(len(airports))

    # Print runtime
    print("Runtime:", round(time.time() - start_time, 1), "s")
