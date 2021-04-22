# As starting point, this requires a list of flights that have either a missing origin or destination,
# a list of flights with origin and destination, and a list of all EU airport ICAO codes. I imported
# them from another python file, but it doesn't really matter how you get them.

# Results in a list with OD pairs: [[LFPG, EHAM], [EHAM, LFPG], ... ]


import numpy as np
import time
import datetime
import csv
import glob
import os
import pandas as pd
import random

## --- Enter your own filepaths here
missing_filepath = r'C:\Users\bcsli\Documents\TU Delft\Second Year\Q3\Project\Missing data'  # Filepath to folder containing missing flights
database_path = r'C:\Users\bcsli\Documents\TU Delft\Second Year\Q3\Project\Recovery dump\database.csv'  # r'C:\Users\bcsli\Documents\TU Delft\Second Year\Q3\Project\All_Flights_2019.csv' # Filepath to database file
save_filepath = r'C:\Users\bcsli\Documents\TU Delft\Second Year\Q3\Project\Recovery dump'  # Filepath where recovered files and log file get saved
eu_ports_filepath = r'C:\Users\bcsli\Downloads\Test-Analysis-Simulation-main\Test-Analysis-Simulation-main\Airports.csv'  # Filepath of list of airports as on GitHub

## --- Move .csv files into lists
complete = pd.read_csv(database_path).values
complete_flight_numbers = np.array([complete[i][0] for i in range(len(complete))])

eu_ports = []
with open(eu_ports_filepath, newline='', errors='replace') as g:
    reader = csv.reader(g)
    for row in reader:
        try:
            eu_ports.append(row[1])
        except IndexError:
            x = row[0]
            x = x.split(",")
            eu_ports.append(x[1])

del eu_ports[0]

## --- Get paths of all files with missing flights
filenames = []

path = missing_filepath
for filename in glob.glob(os.path.join(path, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        filenames.append(filename)

# Initialization for analytics
recovered_counter = 0
missing_counter = 0
len_direct_flights = []

## --- Start of recovery loop --- ##
for j in range(len(filenames)):
    missing = pd.read_csv(filenames[j]).values

    missing_flight_numbers = np.array([missing[i][0] for i in range(len(missing))])
    missing_counter += len(missing)  # Keep track of amount of missing flights

    # Initialize sieve, list for recovered flights and exception counter (can be used to
    # determine the amount of flights recovered)
    sieve = [True for i in range(len(missing))]
    recovered = []
    exceptions = 0

    start = time.time()  # For timing the program

    for i in range(len(missing)):
        if sieve[i]:  # The sieve in action
            flight_number = missing[i][0]

            # Finds the first occurrence of the flight number in the complete flights.
            # Try block is necessary because sometimes flight numbers may not occur
            # in the correct flights.

            correct_entry_indices = np.where(complete_flight_numbers == flight_number)[0]
            if len(correct_entry_indices) == 0:
                exceptions += 1
                continue

            # Gets the indices of all missing flights with the same flight number
            indices = np.where(missing_flight_numbers == flight_number)[0]
            airports = []
            for index in correct_entry_indices:
                port1, port2 = complete[index][1], complete[index][2]
                if port1 not in airports:
                    airports.append(port1)
                if port2 not in airports:
                    airports.append(port2)

            # Additional check to make sure all flights start and end in Europe
            if np.all(airport in airports for airport in eu_ports):  # Check if all airports are in Europe

                for index in indices:
                    if len(airports) == 2:
                        origin, destination = airports[0], airports[1]

                        # This makes sure that the origin and destination are the right way round
                        if origin == missing[index][1] or destination == missing[index][2]:
                            recovered.append([origin, destination])
                        else:
                            recovered.append([destination, origin])

                    else:
                        len_direct_flights.append(len(airports))
                        # Obtain the index of the airport in the missing flight in the airport list variable
                        try:
                            port_index = airports.index(missing[index][1])
                        except ValueError:
                            port_index = airports.index(missing[index][2])

                        if port_index == 0:  # Edge flight
                            add_index = 1
                        elif port_index == len(airports) - 1:  # Edge flight
                            add_index = -2
                        else:  # Center flight, randomly pick airport before or after current airport
                            add_index = port_index + random.choice([-1, 1])

                        origin, destination = airports[add_index], airports[port_index]
                        if origin == missing[index][1] or destination == missing[index][2]:
                            recovered.append([origin, destination])
                        else:
                            recovered.append([destination, origin])

                    # Update the sieve
                    sieve[index] = False

    sieve = np.array(sieve)
    final_recovered = len(np.where(sieve == False)[0])

    still_missing = []
    for i in range(len(missing)):
        if sieve[i]:
            still_missing.append(missing[i])

    recovered_name = r"\recovered" + filenames[j][-12:]
    missing_name = "missing" + filenames[j][-12:]

    with open(save_filepath + recovered_name, 'w', newline="") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["Origin", "Destination"])
        for i in range(len(recovered)):
            thewriter.writerow([recovered[i][0], recovered[i][1]])

    with open('C:\\Users\\bcsli\\Documents\\TU Delft\\Second Year\\Q3\\Project\\Missing dump\\' + missing_name, 'w',
              newline="") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['callsign', 'origin', 'destination'])
        for i in range(len(still_missing)):
            thewriter.writerow([still_missing[i][0], still_missing[i][1], still_missing[i][2]])
    end = time.time()
    print("Finished file (" + str(j + 1) + "/7). Time for section:", end - start)
    recovered_counter += len(recovered)

print("Recovery complete")
print("Total amount of flights recovered:", recovered_counter)
print("Percentage of flights recovered:", str(recovered_counter / missing_counter * 100)[:4] + "%")

## --- Write log file
date = str(datetime.date.today()) + '_' + str(time.strftime("%H:%M:%S"))
file = open(save_filepath + '\Recover_OD_Log_' + date + '.txt', 'w')
file.write('Recover_OD log file:\n \n')
file.write('Date:' + date + '\n \n')
file.write('Recovered files: \n')
names = [" - " + filename[len(path) + 1:] + '\n' for filename in filenames]
file.writelines(names)
file.write('Success rate: ' + str(recovered_counter / missing_counter * 100)[
                              :4] + "%" + f'({recovered_counter}/{missing_counter})\n')
file.write('Percentage direct flights w/ mult. stops: ' + str(len(len_direct_flights) / missing_counter * 100)[
                                                          :4] + "%" + f'({len(len_direct_flights)}/{missing_counter})\n')
file.write(f'Average length direct flights w/ mult. stops: {sum(len_direct_flights) / len(len_direct_flights)}\n')
file.close()
