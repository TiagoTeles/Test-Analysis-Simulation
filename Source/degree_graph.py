"""
TODO
"""

# ---------- Imports ---------- #
import csv
import numpy as np
import matplotlib.pyplot as plt

from Degree_function import node_degree, average_degree
from adjacency import get_matrices


# ---------- Main Program ---------- #
# Define directories
GITDIR = __file__[0:-22]
ASSETDIR = GITDIR + "Assets/"
DIR2019 = GITDIR + "2019_Filtered/"
DIR2020  = GITDIR + "2020_Filtered/"

# Define input file name
AIRPORTDIR = "Airports.csv"             # .CSV containing list of EU airports
FLIGHTFILE = "EU_flights_2020_04.csv"   # .CSV containing list of filtered flights

# Open files
flightsFile = open(DIR2020 + FLIGHTFILE, encoding="utf8")
airportFile = open(ASSETDIR + AIRPORTDIR, encoding="utf8")

# Read files
flight_csv = csv.reader(flightsFile)
airport_csv = csv.reader(airportFile)

# Convert flight database from .CSV to List
flight_list = []
for flight in flight_csv:
    flight_list.append(flight)

del flight_list[0] # Remove legend

# Convert airport codes from .CSV to List
airport_list = []
for airport in airport_csv:
    airport_list.append(str(airport[1]))

del airport_list[0] # Remove legend

# Calculate matrices
adjacency, weight = get_matrices(flight_list)

# Calculate degrees
out_degree_list, in_degree_list, diff_links_list, degree_list = node_degree(weight)
av_degree = average_degree(degree_list)

zero_els = len(degree_list) - np.count_nonzero(degree_list)

# Calculate probability P(K=i)
probability = []
for i in range(1, 300):
    probability.append((np.count_nonzero(degree_list == i)))
xx = range(1, 300)

# Calculate probability P(K>i)
cum_probability = []
for i in range(1, 300):
    cum_probability.append((np.count_nonzero(degree_list >= i)))

# Create the plots
plt.plot(xx,probability, ".")
plt.plot(xx,cum_probability, ".")
plt.yscale("log")
plt.xscale("log")

# Add legend and axis information
plt.title(FLIGHTFILE)
plt.xlabel("Node degree, k")
plt.ylabel("Cumulative probability, P(K(i)>k)")

# Show the plots
plt.show()