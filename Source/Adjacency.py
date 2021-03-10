#importing relevant packages
import numpy as np
import time
import csv

# ----- Setting up the files ----- #

# Define file locations
# Input

GitDir = __file__[0:-19]
AssetDir = GitDir + "Assets/"
Dir2019 = GitDir + "2019_Filtered/"
Dir2020  = GitDir + "2020_Filtered/"

airportDir = "Airports.csv"     # .CSV containing list of EU airports
FlightFile = "EU_flights_2019_01.csv"


# Open files
flightsFile = open(Dir2019 + FlightFile, encoding="utf8")
airportFile = open(AssetDir + airportDir, encoding="utf8")


# Read files
flightsCSV = csv.reader(flightsFile)
airportCSV = csv.reader(airportFile)


# Convert CSV to List
# Airports
AirportList = []
for airport in airportCSV:
    AirportList.append(str(airport[1]))

del (AirportList[0])     # Remove legend











# ----- Defining the function to find adjacency matrix and weight matrix ----- #


def get_adjacency_weight(CSVfile, AirportList):
    #Create empty square matrices for adjacency and weight

    adjacency_matrix = np.zeros((len(AirportList),len(AirportList)))
    weight_matrix = np.zeros((len(AirportList),len(AirportList)))

    #Setting up directed edges
    #entry on a row = origin
    #entry on a column = destination

    '''Example:
       1 2 3
    1 [0,1,0]
    2 [0,0,0]
    3 [1,0,1]
    --> airport 1 has a flight with destination airport 2
    --> airport 3 has a flight with destination airport 1
    '''

    startTime = time.time()
    run = 0
    i = 0
    
    for flight in CSVfile:
        
        #All even entries are just empty
        if i == 0 or ((i%2) != 0):
            i = i + 1
        
        else:
            Origin = AirportList.index(str(flight[1]))
            Destination = AirportList.index(str(flight[2]))

            adjacency_matrix[Origin][Destination] = 1
            weight_matrix[Origin][Destination] += 1
            
            i = i + 1
            run += 1

    #print(adjacency_matrix)
    #print(weight_matrix)

    runTime = time.time() - startTime
    print("Runtime of get_adjacency_weight function is:", round(runTime, 1), "s")
    return adjacency_matrix, weight_matrix


get_adjacency_weight(flightsCSV, AirportList)



