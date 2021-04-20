## It's a mess

import numpy as np
import pandas as pd

complete = []
complete_flight_numbers = []


filenames = [r'C:\Users\bcsli\Documents\Map1.csv']

for filename in filenames:
    flights = pd.read_csv(filename, low_memory=False).values    # Get all the flights
    for i in range(len(flights)):
        flight = flights[i]
        if flight[0] not in complete_flight_numbers:    # Check to see if we already have the flight, might be the wrong thing to do here
            complete_flight_numbers.append(flight[0])
            all_occurences = np.where(flights[0] == flight[0])[0]
            for j in range(len(all_occurences)):
                o = all_occurences[5]
                d = all_occurences[6]
                if(o or d in [complete[i][5] for i in range(len(complete))]) or (o or d in [complete[i][6] for i in range(len(complete))]):     # Attempt at some strange logic
                    complete.append(all_occurences[j])
