"""
Plots a graph of the degree distribution of a given network. The
network is defined by the .CSV files imported.
"""

# ---------- Imports ---------- #
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from degree_function import node_degree, average_degree
from adjacency import get_matrices


# ---------- Main Program ---------- #
# Define directories
GITDIR = __file__[0:-22]
ASSETDIR = GITDIR + "Assets/"
DIR2019 = GITDIR + "2019_Filtered/"
DIR2020  = GITDIR + "2020_Filtered/"

# Define input file name
AIRPORTDIR = "Airports.csv"             # .CSV containing list of EU airports
FLIGHTFILE = "EU_flights_2020_08.csv"   # .CSV containing list of filtered flights

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

# Calculate matrices
adjacency, weight, airports = get_matrices(flight_list)

# Calculate degrees
out_degree_list, in_degree_list, diff_links_list, degree_list = node_degree(weight)
av_degree = average_degree(degree_list)

#Get top 10

degree_list = list(degree_list)

degree_sorted = sorted(degree_list)
top_10 = degree_sorted[:-11:-1]

top_10_index = []
for i in top_10:
    top_10_index.append(degree_list.index(i))

top_10_airports = []

for i in top_10_index:
    top_10_airports.append(airports[i])

print(top_10)
print(top_10_airports)

degree_list = np.array(degree_list)

# Number of airports with degree zero ???

# Calculate probability P(K=i)
probability = []
for i in range(1, np.max(degree_list)):
    probability.append((np.count_nonzero(degree_list == i))/len(airports))
xx = range(1, np.max(degree_list))

# Calculate probability P(K>i)
cum_probability = []
for i in range(1, np.max(degree_list)):
    cum_probability.append((np.count_nonzero(degree_list >= i))/len(airports))

# Create a power law curve fit

degree_list = list(degree_list)

def fct(x, a, b):
    return (x**-a)*np.exp(-x/b)

degree_filtered = list(set(degree_list))

x1 = np.arange(1,len(cum_probability)+1)
popt, trash = curve_fit(fct, x1, cum_probability, maxfev=2000)
a, b = popt

power_law = fct(x1,a,b)

degree_list = np.array(degree_list)


# Create the plots
#plt.plot(xx,probability, ".")
plt.plot(xx,cum_probability, ".")
plt.plot(x1,power_law, linestyle = "--")
plt.yscale("log")
plt.xscale("log")

# Add legend and axis information
plt.title("cumulative degree distribution for " + FLIGHTFILE)
plt.xlabel("Node degree, k")
plt.ylabel("P(K(i)$\geqslant$k)")

# Show the plots
plt.show()
