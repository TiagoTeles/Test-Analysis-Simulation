import numpy as np
import time
import csv
import matplotlib.pyplot as plt 

from Degree_function import node_degree, average_degree
from Adjacency import getMatrices




# Define directories
gitDir = __file__[0:-14]
assetDir = gitDir + "Assets/"
dir2019 = gitDir + "2019_Filtered/"
dir2020  = gitDir + "2020_Filtered/"

# Define input file name
airportDir = "Airports.csv"             # .CSV containing list of EU airports
flightFile = "EU_flights_2019_05.csv"   # .CSV containing list of filtered flights

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
adjacency, weight = getMatrices(flightList, airportList)


out_degree_list, in_degree_list, diff_links_list, degree_list = node_degree(weight)
av_degree = average_degree(degree_list)

for i in range(len(degree_list)):
    airport = airportList[i]
    degree = degree_list[i]
    #print('Aiport =', airport, '+ degree:', degree)


zero_els = len(degree_list) - np.count_nonzero(degree_list)

#print(weight)
#print(degree_list)
print(av_degree)
#print(len(degree_list))
#print(zero_els)


occurence = []
for i in range(300):
    occurence.append((np.count_nonzero(degree_list == i)/len(airportList)))
xx = range(300)

plt.plot(xx,occurence)
plt.yscale("log")
plt.xscale("log")
plt.show()




