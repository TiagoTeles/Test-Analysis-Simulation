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
def getMatrices(flightList, airportList):
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
    n = len(airportList)
    adjacencyMatrix = np.zeros((n, n), int)
    weightMatrix = np.zeros((n, n), int)
    
    # Iterate over flights
    for flight in flightList:
        if flight != []:
            # Determine indices
            originIndex = airportList.index(str(flight[1]))
            destinationIndex = airportList.index(str(flight[2]))
        
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
airportDir = "Airports.csv"             # .CSV containing list of EU airports
flightFile = "EU_flights_2019_01.csv"   # .CSV containing list of filtered flights

# Open files
flightsFile = open(dir2019 + flightFile, encoding="utf8")
airportFile = open(assetDir + airportDir, encoding="utf8")

# Read files
flightsCSV = csv.reader(flightsFile)
airportCSV = csv.reader(airportFile)

# Convert flight database from .CSV to List
flightList = []
for flight in flightsCSV:
    flightList.append(flight)

del (flightList[0]) # Remove legend

# Convert airport codes from .CSV to List
airportList = []
for airport in airportCSV:
    airportList.append(str(airport[1]))

del (airportList[0]) # Remove legend

# Calculate Matrices
startTime = time.time()
print(getMatrices(flightList, airportList))

# Print runtime
print("Runtime:", round(time.time() - startTime, 1), "s")
