# As starting point, this requires a list of flights that have either a missing origin or destination,
# a list of flights with origin and destination, and a list of all EU airport ICAO codes. I imported
# them from another python file, but it doesn't really matter how you get them.

# Results in a list with OD pairs: [[LFPG, EHAM], [EHAM, LFPG], ... ]

# In the worst case, it could take up to 2 hours to process 400000 flights.


import numpy as np
from get_missing import missing, complete, eu_ports
import time


# missing =  [["aa11", '', '', '', '', 'LFPG', ''], ["aa11", '', '', '', '', '', 'LFPG'], ["aa11", '', '', '', '', '', 'EHAM']]
# complete = [['aa11', '', '', '', '', 'LFPG', 'EHAM']]


# Lists with just flight numbers make everything a bit easier
complete_flight_numbers = [complete[i][0] for i in range(len(complete))]
missing_flight_numbers = np.array([missing[i][0] for i in range(len(missing))])


# Initialize sieve, list for recovered flights and exception counter (can be used to
# determine the amount of flights recovered)
sieve = [True for i in range(len(missing))]
recovered = []
exceptions = 0

start = time.time()  # For timing the program

for i in range(1000):  # When doing the entire list, change 1000 to len(missing)
    if sieve[i]:  # The sieve in action
        flight_number = missing[i][0]

        # Gets the indices of all missing flights with the same flight number
        indices = np.where(missing_flight_numbers == flight_number)[0]

        # Finds the first occurrence of the flight number in the complete flights.
        # Try block is necessary because sometimes flight numbers may not occur
        # in the correct flights.
        try:
            correct_entry_index = complete_flight_numbers.index(flight_number)
        except ValueError:
            exceptions += 1
            continue

        origin, destination = complete[correct_entry_index][5], complete[correct_entry_index][6]

        # Additional check to make sure all flights start and end in Europe
        if origin in eu_ports and destination in eu_ports:

            for j in range(len(indices)):
                # This makes sure that the origin and destination are the right way round
                if origin == missing[indices[j]][5] or destination == missing[indices[j]][6]:
                    recovered.append([origin, destination])
                else:
                    recovered.append([destination, origin])

                # Update the sieve
                sieve[indices[j]] = False

end = time.time()

print(end-start)


