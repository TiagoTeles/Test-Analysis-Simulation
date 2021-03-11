# Node strength

import numpy as np
import time
import csv

from Adjacency import getMatrices


def get_Node_strength(weightMatrix):

    node_strength = []
    
    for row in weightMatrix:
        node_strength.append(sum(row))

    return node_strength


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
adjacency, weight = getMatrices(flightList)

strength = get_Node_strength(weight)
print(strength)
