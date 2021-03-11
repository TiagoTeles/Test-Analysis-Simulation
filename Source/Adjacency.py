## ---------- Imports ---------- ##
import numpy as np
import time
import csv

"""
This script imports the relevant data from .CSV files, converts it to lists 
and creates directed adjacency and weight matrices from those lists.

The Flights.CSV file has the following structure:
Callsign, Origin, Destination

The Airports.CSV file has the following structure:
Size, ICAO Code, IATA Code, Name, Latitude, Longitude, Country
"""

## ---------- Function Definitions ---------- ##
def getMatrices(flightList):
    # ----- Defining the function to find adjacency matrix and weight matrix ----- #
    """ Constructs directed adjacency and weight matrices from the data provided.
        THe row index corresponds to index of the origin airport, the column index
        corresponds to the destination airport.

    Arguments:
        flightList {List} -- List of flights to be considered
        airportList {List} -- List of airports to be considered

    Returns:
        ndarray -- Adjacency matrix
        ndarray -- Weight matrix
    """

    # Create empty matrices
    used_airports = []
    for flight in flightList:
        used_airports.append(flight[1])
        used_airports.append(flight[2])
    airportset = set(used_airports)
    print(len(airportset))
    
    airports = list(airportset)
    airports.sort()
    
    print(len(airports))
    print(airports)
    
    n = len(airports)
    adjacencyMatrix = np.zeros((n, n), int)
    weightMatrix = np.zeros((n, n), int)
    
    # Iterate over flights
    for flight in flightList:
        # Determine indices
        originIndex = airports.index(str(flight[1]))
        destinationIndex = airports.index(str(flight[2]))
        
        # Update matrices
        adjacencyMatrix[originIndex][destinationIndex] = 1
        weightMatrix[originIndex][destinationIndex] += 1

    return adjacencyMatrix, weightMatrix


## ---------- Main Program ---------- ##

# Define directories
gitDir = __file__[0:-19]
assetDir = gitDir + "Assets/"
dir2019 = gitDir + "2019_Filtered/"
dir2020  = gitDir + "2020_Filtered/"

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
adjacency, weight = getMatrices(flightList)

# Print runtime
print("Runtime:", round(time.time() - startTime, 1), "s")
