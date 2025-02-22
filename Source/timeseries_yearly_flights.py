import matplotlib.pyplot as plt
import numpy as np
import csv


# Define function
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
DIR2019 = __file__[0:-35] + "Combined_2019_new/"
DIR2020 = __file__[0:-35] + "Combined_2020_new/"

DIR2020_I = __file__[0:-35] + "2020_filtered/"
DIR2019_I = __file__[0:-35] + "2019_filtered/"


# Get the 2020 files  

freq1 = get_frequencies(DIR2020 + "Combined_2020_01_b.csv")
freq2 = get_frequencies(DIR2020 + "Combined_2020_02_b.csv")
freq3 = get_frequencies(DIR2020 + "Combined_2020_03_b.csv")
freq4 = get_frequencies(DIR2020 + "Combined_2020_04_b.csv")
freq5 = get_frequencies(DIR2020 + "Combined_2020_05_b.csv")
freq6 = get_frequencies(DIR2020 + "Combined_2020_06_b.csv")
freq7 = get_frequencies(DIR2020 + "Combined_2020_07_b.csv")
freq8 = get_frequencies(DIR2020 + "Combined_2020_08_b.csv")
freq9 = get_frequencies(DIR2020 + "Combined_2020_09_b.csv")
freq10 = get_frequencies(DIR2020 + "Combined_2020_10_b.csv")
freq11 = get_frequencies(DIR2020 + "Combined_2020_11_b.csv")
freq12 = get_frequencies(DIR2020 + "Combined_2020_12_b.csv")

frequencies1 = freq1 + freq2 + freq3 + freq4 + freq5 + freq6 + freq7 + freq8 + freq9 + freq10 + freq11 + freq12

# Get 2019 files

freq01 = get_frequencies(DIR2019 + "Combined_2019_01_b.csv")
freq02 = get_frequencies(DIR2019 + "Combined_2019_02_b.csv")
freq03 = get_frequencies(DIR2019 + "Combined_2019_03_b.csv")
freq04 = get_frequencies(DIR2019 + "Combined_2019_04_b.csv")
freq05 = get_frequencies(DIR2019 + "Combined_2019_05_b.csv")
freq06 = get_frequencies(DIR2019 + "Combined_2019_06_b.csv")
freq07 = get_frequencies(DIR2019 + "Combined_2019_07_b.csv")
freq08 = get_frequencies(DIR2019 + "Combined_2019_08_b.csv")
freq09 = get_frequencies(DIR2019 + "Combined_2019_09_b.csv")
freq010 = get_frequencies(DIR2019 + "Combined_2019_10_b.csv")
freq011 = get_frequencies(DIR2019 + "Combined_2019_11_b.csv")
freq012 = get_frequencies(DIR2019 + "Combined_2019_12_b.csv")

freq09[21] = int((freq09[20]+freq09[22])/2)

frequencies2 = freq01 + freq02 + freq03 + freq04 + freq05 + freq06 + freq07 + freq08 + freq09 + freq010 + freq011 + freq012
# print(freq09)

# Calculate averages

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

freq11 = get_frequencies(DIR2020_I + "inter_flights_2020_01.csv")
freq12 = get_frequencies(DIR2020_I + "inter_flights_2020_02.csv")
freq13 = get_frequencies(DIR2020_I + "inter_flights_2020_03.csv")
freq14 = get_frequencies(DIR2020_I + "inter_flights_2020_04.csv")
freq15 = get_frequencies(DIR2020_I + "inter_flights_2020_05.csv")
freq16 = get_frequencies(DIR2020_I + "inter_flights_2020_06.csv")
freq17 = get_frequencies(DIR2020_I + "inter_flights_2020_07.csv")
freq18 = get_frequencies(DIR2020_I + "inter_flights_2020_08.csv")
freq19 = get_frequencies(DIR2020_I + "inter_flights_2020_09.csv")
freq110 = get_frequencies(DIR2020_I + "inter_flights_2020_10.csv")
freq111 = get_frequencies(DIR2020_I + "inter_flights_2020_11.csv")
freq112 = get_frequencies(DIR2020_I + "inter_flights_2020_12.csv")

frequencies3 = freq11 + freq12 + freq13 + freq14 + freq15 + freq16 + freq17 + freq18 + freq19 + freq110 + freq111 + freq112

# Get 2019 files

freq21 = get_frequencies(DIR2019_I + "inter_flights_2019_01.csv")
freq22 = get_frequencies(DIR2019_I + "inter_flights_2019_02.csv")
freq23 = get_frequencies(DIR2019_I + "inter_flights_2019_03.csv")
freq24 = get_frequencies(DIR2019_I + "inter_flights_2019_04.csv")
freq25 = get_frequencies(DIR2019_I + "inter_flights_2019_05.csv")
freq26 = get_frequencies(DIR2019_I + "inter_flights_2019_06.csv")
freq27 = get_frequencies(DIR2019_I + "inter_flights_2019_07.csv")
freq28 = get_frequencies(DIR2019_I + "inter_flights_2019_08.csv")
freq29 = get_frequencies(DIR2019_I + "inter_flights_2019_09.csv")
freq210 = get_frequencies(DIR2019_I + "inter_flights_2019_10.csv")
freq211 = get_frequencies(DIR2019_I + "inter_flights_2019_11.csv")
freq212 = get_frequencies(DIR2019_I + "inter_flights_2019_12.csv")

freq29[21] = int((freq29[20]+freq29[22])/2)

frequencies4 = freq21 + freq22 + freq23 + freq24 + freq25 + freq26 + freq27 + freq28 + freq29 + freq210 + freq211 + freq212

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
plt.rcParams['font.size'] = '13'
plt.rcParams['legend.framealpha'] = '0.4'

plt.plot(x2,frequencies2, alpha = 0.3, color = "darkorange", label = "2019: Daily # flights")
plt.plot(x2,day_avg2, color = "darkorange", linestyle = '-', label = "2019: 7 day average", linewidth = 3)
plt.plot(x,frequencies1, alpha = 0.3, color = "mediumblue", label = "2020: Daily # flights")
plt.plot(x,day_avg, color = "mediumblue", linestyle = '-', label = "2020: 7 day average", linewidth = 3)
plt.axvline(x=71, color = 'red', linestyle = '--')
plt.xticks([0,31,59,90,120,151,181,212,243,273,304,334], ["January 1st","February 1st","March 1st", "April 1st","May 1st", "June 1st", "July 1st", "August 1st", "September 1st", "October 1st", "November 1st", "December 1st"], rotation = 50)
plt.xlim([0,len(frequencies1)])
plt.text(75, 15500, 'March 11, 2020: WHO declared pandemic', color = 'red', fontsize=16)
# plt.title("Daily number of European flights", fontsize=18)
plt.xlabel("Day", fontsize=16)
plt.ylabel("Number of flights", fontsize=16)
plt.legend()
plt.grid(axis="x", linestyle="--")
plt.tight_layout()
plt.show()


plt.plot(x4,frequencies4, alpha = 0.3, color = "darkorange", label = "2019: Daily # flights")
plt.plot(x4,day_avg4, color = "darkorange", label = "2019: 7 day average", linewidth = 3)
plt.plot(x3,frequencies3, alpha = 0.3, color = "mediumblue", label = "2020: Daily # flights")
plt.plot(x3,day_avg3, color = "mediumblue", label = "2020: 7 day average", linewidth = 3)
plt.axvline(x=71, color = 'red', linestyle = '--')
plt.xticks([0,31,59,90,120,151,181,212,243,273,304,334], ["January 1st","February 1st","March 1st", "April 1st","May 1st","June 1st","July 1st","August 1st", "September 1st", "October 1st", "November 1st", "December 1st"], rotation = 50)
plt.xlim([0,len(frequencies1)])
plt.text(75, 1660, 'March 11, 2020: WHO declared pandemic', color = 'red', fontsize=16)
# plt.title("Daily number of intercontinental flights", fontsize=18)
plt.xlabel("Day", fontsize=16)
plt.ylabel("Number of flights", fontsize=16)
plt.legend(loc='lower left')
plt.grid(axis = "x", linestyle = "--")
plt.tight_layout()
plt.show()


# percentage comparison
EU_comp = 1 - sum(freq4)/sum(freq04)
Int_comp = 1 - sum(freq14)/sum(freq24)

print(EU_comp)
print(Int_comp)
