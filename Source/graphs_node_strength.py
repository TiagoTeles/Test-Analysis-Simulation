# Imports
import csv
import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit

from degree_function import node_degree, average_degree
from adjacency import get_matrices
from Node_strength_function import get_Node_strength

# ---------- Main Program ---------- #
# Define directories
GITDIR = __file__[0:-30]
ASSETDIR = GITDIR + "Assets/"
DIR2019 = GITDIR + "2019_Filtered/"
DIR2020  = GITDIR + "2020_Filtered/"

# Define input file name
AIRPORTDIR = "Airports.csv"             # .CSV containing list of EU airports
FLIGHTFILE = "EU_flights_2020_08.csv"   # .CSV containing list of filtered flights

# Open files
airportFile = open(ASSETDIR + AIRPORTDIR, encoding="utf8")
flightsFile = open(DIR2020 + FLIGHTFILE, encoding="utf8")

# Read files
airport_csv = csv.reader(airportFile)
flight_csv = csv.reader(flightsFile)

# Convert flight database from .CSV to List
flight_list = []
for flight in flight_csv:
    flight_list.append(flight)

del flight_list[0] # Remove legend

# Calculate matrices
adjacency, weight, airports = get_matrices(flight_list)

# Calculate degrees
out_degree_list, in_degree_list, diff_links_list, degree_list = node_degree(weight)
av_degree = average_degree(degree_list)

#Now get the node strengths for the data
in_strength, out_strength, total_strength = get_Node_strength(weight)

#print('\n', total_strength)

x2 = np.arange(len(airports))

# #Get top 10, only works for 1 month --> indices change per month
strength_sorted = sorted(total_strength, reverse=True)
# top_10_1 = strength_sorted[0:10]
#
# top_10_index1 = []
# for i in top_10_1:
#     top_10_index1.append(total_strength.index(i))
#
# top_10_airports1 = []
#
# for i in top_10_index1:
#     top_10_airports1.append(airports[i])
#
# print('The top 10 airports based on node strength are: ', top_10_airports1)
# print('With their respective degrees: ', top_10_1)



# Create the plots
# This plot shows that there are a lot of airports with a small node strength and only a few with a large node strength
# This is equivalent to 'Weighted degree' in some definitions
plt.figure()
plt.plot(x2,strength_sorted, ".")
plt.yscale("linear")
plt.xscale("linear")

# Add legend and axis information
plt.title("Node strength for the airports in " + FLIGHTFILE)
plt.xlabel("Just numbers to plot")
plt.ylabel("Node strength")

# Show the plot
plt.show()