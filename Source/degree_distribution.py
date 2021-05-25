"""
Plots a graph of the degree distribution of a given network. The
network is defined by the .CSV files imported.
"""

# ---------- Imports ---------- #
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time

from degree_function import node_degree, average_degree
from adjacency import get_matrices

# ---------- Function --------- #
def get_average_degree(filename):
    # ----- Defining the function to find the average degree per month ----- #
    """ Constructs average degree per month (data file)

    Arguments:
        Filename -- CSV file with flight data

    Returns:
        Value -- average node degree
    """
    flights_file = open(filename, encoding="utf8")

    flights_csv = csv.reader(flights_file)

    flight_list = []
    for flight in flights_csv:
        flight_list.append(flight)

    del flight_list[0]  # Remove legend

    # Calculate matrices
    adjacency, weight, airports = get_matrices(flight_list)

    # Calculate degrees
    out_degree_list, in_degree_list, diff_links_list, degree_list = node_degree(weight)

    av_degree = average_degree(degree_list)

    return av_degree



# ---------- Main Program ---------- #

start_time = time.time()
# Define directories
GITDIR = __file__[0:-23]
ASSETDIR = GITDIR + "Assets/"
DIR2019 = GITDIR + "Combined_2019_new/"
DIR2020  = GITDIR + "Combined_2020_new/"

# Define input file name
AIRPORTDIR = "Airports.csv"             # .CSV containing list of EU airports
FLIGHTFILE = "Combined_2019_04_b.csv"   # .CSV containing list of filtered flights

# Open files
airportFile = open(ASSETDIR + AIRPORTDIR, encoding="utf8")
flightsFile = open(DIR2019 + FLIGHTFILE, encoding="utf8")

# Read files
airport_csv = csv.reader(airportFile)
flight_csv = csv.reader(flightsFile)



''' Get cumulative degree probability for specific month'''
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

#Get top 10, only works for 1 month --> indices change for every month
degree_list = list(degree_list)

degree_sorted = sorted(degree_list)
# top_10 = degree_sorted[:-11:-1]
#
# top_10_index = []
# for i in top_10:
#     top_10_index.append(degree_list.index(i))
#
# top_10_airports = []
#
# for i in top_10_index:
#     top_10_airports.append(airports[i])
# print('The top 10 airports based on degree are: ', top_10_airports)
# print('With their respective degrees: ', top_10,'\n')


#Convert back to array
degree_list = np.array(degree_list)


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

equation = r"$P(K(i)\geqslant k)$ = " + '$k^{-' + str(round(a,3)) + '}$ * $e^{-k/' + str(round(b,3)) +'}$'

plt.rcParams['font.size'] = '13'
plt.rcParams['figure.figsize'] = 7, 5

# Create the plots
#plt.plot(xx,probability, ".")
#plt.subplot(211)
plt.plot(xx,cum_probability, ".", color = 'darkorange', label = r"$P(K(i)\geqslant k)$")
plt.plot(x1,power_law, linestyle = "--", color = 'black', label = "Power law approximation")
# plt.text(50, 50, equation, color = 'black')
# plt.text(75, 10000, 'March 11: WHO declared pandemic', color = 'red')
plt.yscale("log")
plt.xscale("log")

# Add legend and axis information
# plt.title("Cumulative degree distribution for the april 2020 network", fontsize='15')
# plt.title("cumulative degree distribution for " + FLIGHTFILE)
plt.xlabel("Node degree, " + r"$k$")
# plt.ylabel("P(K(i)$\geqslant$k)")
plt.ylabel(r"$P(K(i)\geqslant k)$")
plt.text(1, 0.2, equation, color = 'black')
plt.legend(loc='lower left')
plt.tight_layout()

# Show the plot
plt.show()


# ''' Time series for average degree'''
#
# #2019
#
# files_2019 = []
# for i in range(1,13):
#     if i < 10:
#         name = DIR2019 + "Combined_2019_0" + str(i) + "_b.csv"
#     else:
#         name = DIR2019 + "Combined_2019_" + str(i) + "_b.csv"
#
#     files_2019.append(name)
#
#
# av_2019 = []
#
# for i in files_2019:
#     av_2019.append(get_average_degree(i))
#
#
# #2020
# files_2020 = []
# for i in range(1,13):
#     if i < 10:
#         name = DIR2020 + "Combined_2020_0" + str(i) + "_b.csv"
#     else:
#         name = DIR2020 + "Combined_2020_" + str(i) + "_b.csv"
#
#     files_2020.append(name)
#
# av_2020 = []
#
# for i in files_2020:
#     av_2020.append(get_average_degree(i))
#
#
# xx = np.arange(1,13)
#
# print('Runtime = ', time.time()-start_time )
# # Graph plotting
# # plt.figure()
# plt.plot(xx,av_2019,  color = "darkorange", label = "2019", marker = '*')
# plt.plot(xx,av_2020, color = "mediumblue", label = "2020", marker = 'x')
# plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12], ["January","February","March", "April","May","June","July","August", "September", "October", "November", "December"], rotation = 45)
# plt.title("Average node degree per month")
# plt.xlabel("Month")
# plt.ylabel("Average node degree")
# plt.legend()
# plt.grid(axis="x", linestyle="--")
# plt.tight_layout()
# # show plots
# plt.show()
