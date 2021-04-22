""" This script creates a list for both years containing all unique
    combinations of callsign - origin - destination, which is needed
    for the OD recovery for the incomplete flights, which is executed
    by Benjamin"""


# ---------- Imports ---------- #
import numpy as np
import pandas as pd
import csv


# ---------- Function Definitions ---------- #
def get_filename(git_dir, year, month, inter):
    """
    Determines the filename based
    on the parameters given.

    Arguments:
        git_dir (String): Base directory
        year (int): Year teh data was collected
        month (int): Month the data was collected
        inter (Boolean): Whether the data is from europe or intercontinantal

    Returns:
        filename (String): Name of the file
    """

    month_str = str(month).zfill(2)
    year_str = str(year)

    if not inter:
        filename = "{0}{1}_Filtered//EU_flights_{1}_{2}.csv".format(git_dir, year_str, month_str)
    else:
        filename = "{0}{1}_Filtered//Inter_flights_{1}_{2}.csv".format(git_dir, year_str, month_str)

    return filename


## ---------- Main Program ---------- ##
if __name__ == "__main__":
    # Define directories
    GIT_DIR = __file__[0:-27]
    ASSET_DIR = GIT_DIR + "Assets/"

# Define output file names
LIST_2019 = "All_Flights_2019.csv"
LIST_2020 = "All_Flights_2020.csv"

# Get lists of filenames to be used
filenames2019 = []
filenames2020 = []
for month in range(1, 12 + 1):

    filename_2019 = get_filename(GIT_DIR, 2019, month, False)
    filename_2020 = get_filename(GIT_DIR, 2020, month, False)

    filenames2019.append(filename_2019)
    filenames2020.append(filename_2020)

# Open these files & add the contents to new lists
complete_flight_numbers2019 = []
for filename in filenames2019:
    flights = pd.read_csv(filename, low_memory=False).values    # Get all the flights
    print('Adding', int(len(flights)), 'entries')
    for i in range(len(flights)):
        flight = flights[i]
        complete_flight_numbers2019.append(tuple(flight[0:3]))

complete_flight_numbers2020 = []
for filename in filenames2020:
    flights = pd.read_csv(filename, low_memory=False).values    # Get all the flights
    print('Adding', int(len(flights)), 'entries')
    for i in range(len(flights)):
        flight = flights[i]
        complete_flight_numbers2020.append(tuple(flight[0:3]))

# Remove all duplicates for each year
result2019 = list(set(complete_flight_numbers2019))
result2020 = list(set(complete_flight_numbers2020))

# Export the results to .csv files
with open(ASSET_DIR + LIST_2019, 'w', newline="") as f:
    the_writer = csv.writer(f)
    for row in result2019:
        the_writer.writerow(list(row))

with open(ASSET_DIR + LIST_2020, 'w', newline="") as f:
    the_writer = csv.writer(f)
    for row in result2020:
        the_writer.writerow(list(row))

