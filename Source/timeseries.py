import matplotlib.pyplot as plt
import numpy as np
import csv


#Define function
def get_frequencies(filename):
    # ----- Defining the function to find the number of flights per day ----- #
    """ Constructs the number of flights per day from a data file

    Arguments:
        Filename -- CSV file with flight data

    Returns:
        list -- List of #flights per day 
    """
    flights_file = open(filename, encoding = "utf8")

    flights_csv = csv.reader(flights_file)

    flights_days = []
    for flight in flights_csv:
        flights_days.append(flight[-1][8:])

        
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
            
    #Add the data for the very last day in the list
            
    frequencies.append(i)
    
    return frequencies




# ----- European flights ----- #
# Create directories
DIR2019 = __file__[0:-20] + "2019_Filtered/"
DIR2020 = __file__[0:-20] + "2020_Filtered/"

# Get the 2020 files  

freq1 = get_frequencies(DIR2020 + "EU_flights_2020_01.csv")
freq2 = get_frequencies(DIR2020 + "EU_flights_2020_02.csv")
freq3 = get_frequencies(DIR2020 + "EU_flights_2020_03.csv")
freq4 = get_frequencies(DIR2020 + "EU_flights_2020_04.csv")
freq5 = get_frequencies(DIR2020 + "EU_flights_2020_05.csv")
freq6 = get_frequencies(DIR2020 + "EU_flights_2020_06.csv")
freq7 = get_frequencies(DIR2020 + "EU_flights_2020_07.csv")

frequencies1 = freq1 + freq2 + freq3 + freq4 + freq5 + freq6 + freq7

# Get 2019 files

freq01 = get_frequencies(DIR2019 + "EU_flights_2019_01.csv")
freq02 = get_frequencies(DIR2019 + "EU_flights_2019_02.csv")
freq03 = get_frequencies(DIR2019 + "EU_flights_2019_03.csv")
freq04 = get_frequencies(DIR2019 + "EU_flights_2019_04.csv")
freq05 = get_frequencies(DIR2019 + "EU_flights_2019_05.csv")
freq06 = get_frequencies(DIR2019 + "EU_flights_2019_06.csv")
freq07 = get_frequencies(DIR2019 + "EU_flights_2019_07.csv")

frequencies2 = freq01 + freq02 + freq03 + freq04 + freq05 + freq06 + freq07

#Calculate averages

day_avg = []
for i in range(7):
    day_avg.append(sum(frequencies1[0:i+1]) / (i+1))
for i in range(len(frequencies1) - 7):
    day_avg.append(sum(frequencies1[i:i+7]) / 7)

day_avg2 = []
for i in range(7):
    day_avg2.append(sum(frequencies2[0:i+1]) / (i+1))
for i in range(len(frequencies2) - 7):
    day_avg2.append(sum(frequencies2[i:i+7]) / 7)
    

x = np.linspace(1,len(frequencies1),len(frequencies1))
x2 = np.linspace(1,len(frequencies2),len(frequencies2))

# ----- Intercontinental flights ----- #
# Get the 2020 files  

freq11 = get_frequencies(DIR2020 + "inter_flights_2020_01.csv")
freq12 = get_frequencies(DIR2020 + "inter_flights_2020_02.csv")
freq13 = get_frequencies(DIR2020 + "inter_flights_2020_03.csv")
freq14 = get_frequencies(DIR2020 + "inter_flights_2020_04.csv")
freq15 = get_frequencies(DIR2020 + "inter_flights_2020_05.csv")
freq16 = get_frequencies(DIR2020 + "inter_flights_2020_06.csv")
freq17 = get_frequencies(DIR2020 + "inter_flights_2020_07.csv")

frequencies3 = freq11 + freq12 + freq13 + freq14 + freq15 + freq16 + freq17

# Get 2019 files

freq21 = get_frequencies(DIR2019 + "inter_flights_2019_01.csv")
freq22 = get_frequencies(DIR2019 + "inter_flights_2019_02.csv")
freq23 = get_frequencies(DIR2019 + "inter_flights_2019_03.csv")
freq24 = get_frequencies(DIR2019 + "inter_flights_2019_04.csv")
freq25 = get_frequencies(DIR2019 + "inter_flights_2019_05.csv")
freq26 = get_frequencies(DIR2019 + "inter_flights_2019_06.csv")
freq27 = get_frequencies(DIR2019 + "inter_flights_2019_07.csv")

frequencies4 = freq21 + freq22 + freq23 + freq24 + freq25 + freq26 + freq27

#Calculate averages

day_avg3 = []
for i in range(7):
    day_avg3.append(sum(frequencies3[0:i+1]) / (i+1))
for i in range(len(frequencies3) - 7):
    day_avg3.append(sum(frequencies3[i:i+7]) / 7)

day_avg4 = []
for i in range(7):
    day_avg4.append(sum(frequencies4[0:i+1]) / (i+1))
for i in range(len(frequencies4) - 7):
    day_avg4.append(sum(frequencies4[i:i+7]) / 7)
    

x3 = np.linspace(1,len(frequencies3),len(frequencies3))
x4 = np.linspace(1,len(frequencies4),len(frequencies4))

# ----- Plotting ----- #

#fig, (ax1, ax2) = plt.subplots(1, 2)'

plt.subplot(1, 2, 1)
plt.plot(x2,frequencies2, alpha = 0.3, color = "darkorange", label = "2019: Daily # flights")
plt.plot(x2,day_avg2, color = "darkorange", label = "2019: 7 day average", linewidth = 3)
plt.plot(x,frequencies1, alpha = 0.3, color = "dodgerblue", label = "2020: Daily # flights")
plt.plot(x,day_avg, color = "dodgerblue", label = "2020: 7 day average", linewidth = 3)
plt.axvline(x=71, color = 'red', linestyle = '--')
plt.xticks([0,31,59,90,120,151,181,212,241], ["January","February","March", "April","May","June","July","August"], rotation = 45)
plt.xlim([0,len(frequencies1)])
plt.text(75, 10000, 'March 11: WHO declared pandemic', color = 'red')
plt.title("Daily number of European flights")
#plt.xlabel("Date")
plt.ylabel("Number of flights")
plt.legend()
plt.grid(axis = "x", linestyle = "--")

plt.subplot(1, 2, 2)
plt.plot(x4,frequencies4, alpha = 0.3, color = "darkorange", label = "2019: Daily # flights")
plt.plot(x4,day_avg4, color = "darkorange", label = "2019: 7 day average", linewidth = 3)
plt.plot(x3,frequencies3, alpha = 0.3, color = "dodgerblue", label = "2020: Daily # flights")
plt.plot(x3,day_avg3, color = "dodgerblue", label = "2020: 7 day average", linewidth = 3)
plt.axvline(x=71, color = 'red', linestyle = '--')
plt.xticks([0,31,59,90,120,151,181,212,241], ["January","February","March", "April","May","June","July","August"], rotation = 45)
plt.xlim([0,len(frequencies1)])
plt.text(75, 1660, 'March 11: WHO declared pandemic', color = 'red')
plt.title("Daily number of intercontinental flights")
#plt.xlabel("Date")
plt.ylabel("Number of flights")
plt.legend()
plt.grid(axis = "x", linestyle = "--")
plt.show()


