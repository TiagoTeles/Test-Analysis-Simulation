import matplotlib.pyplot as plt
import numpy as np
import csv

def get_frequencies(filename):
    flights_file = open(filename, encoding = "utf8")

    flights_csv = csv.reader(flights_file)

    flights_days = []

    for flight in flights_csv:
        flights_days.append(flight[-1][0:2])

    del flights_days[0]

    for flight in flights_days:
        flight = int(flight)

    flights_days.sort()

    day = flights_days[0]
    i = 0
    frequencies = []

    for flight in flights_days:
        if flight == day:
            i += 1
        else:
            day = flight
            frequencies.append(i)
            i = 0

    return frequencies

freq1 = get_frequencies("EU_flights_2020_01_days.csv")
freq2 = get_frequencies("EU_flights_2020_02_days.csv")
freq3 = get_frequencies("EU_flights_2020_03_days.csv")
freq4 = get_frequencies("EU_flights_2020_04_days.csv")
freq5 = get_frequencies("EU_flights_2020_05_days.csv")
freq6 = get_frequencies("EU_flights_2020_06_days.csv")
freq7 = get_frequencies("EU_flights_2020_07_days.csv")

frequencies = freq1 + freq2 + freq3 + freq4 + freq5 + freq6 + freq7

day_avg = []
for i in range(7):
    day_avg.append(sum(frequencies[0:i+1]) / (i+1))
for i in range(len(frequencies) - 7):
    day_avg.append(sum(frequencies[i:i+7]) / 7)

print(len(frequencies))
print(len(day_avg))

x = np.linspace(1,len(frequencies),len(frequencies))

plt.plot(x,frequencies, alpha = 0.3, color = "blue", label = "Daily number")
plt.plot(x,day_avg, color = "blue", label = "7 day average", linewidth = 3)
plt.xticks([0,31,59,90,120,151,181,212], ["January","February","March","April","May","June","July"], rotation = 45)
plt.xlim([0,len(frequencies)])
plt.title("Daily number of flights in 2020")
plt.xlabel("Date")
plt.ylabel("Number of flights")
plt.legend()
plt.grid(axis = "x", linestyle = "--")
plt.show()



