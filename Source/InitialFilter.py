## ---------- Imports ---------- ##
import csv
import time

"""
This script filters out flights that do not belong in the data analysis. The
criteria for inclusion are the following:
- Has Origin or Destination
- Origin or Destination is in Europe (ICAO E, B or L)
- Airport in Europe is not military
- Origin or Destinations ICAO codes do not contain a number
- Is not a cargo flight

The input .CSV file has the following structure:
Callsign, Flight Number, Transponder Code, A/C Registration, Type Code,
Origin, Destination, First Seen, Last Seen, Day, Latitude_1, Longitude_1,
Altitude_1, Latitude_2, Longitude_2, Altitude_2
"""

## ---------- Function definitions ---------- ##
def containsNumber(s):
    """ Checks if input contains a number

    Arguments:
        s {String}-- Argument to be checked

    Returns:
        Boolean -- True if value contains a number
    """

    for c in s:
        try:
            float(c)
            return True
        except:
            pass

    return False


def isMilitaryInEu(icaoCode, letterSet, airportDatabase):
    """ Checks if ICAO code is from an European military airport

    Arguments:
        icaoCode {String} -- ICAO code of the airport to be checked
        letterSet {List} -- First letter of the airports to consider
        airportDatabase {List} -- List of civilian airports

    Returns:
        Boolean -- True if the airport is military and in Europe
    """

    return (icaoCode[0] in letterSet) and (icaoCode not in airportDatabase)


## ---------- Main Program ---------- ##
startTime = time.time()                             # Define start time

# Define directories
gitDir = __file__[0:-23]
assetDir = gitDir + "Assets/"
dir2019 = gitDir + "2019_Filtered/"
dir2020 = gitDir + "2020_Filtered/"
misDir = gitDir + "Missing_Flights/"

# Define input file names
#flightsDir = "C:/Users/mathi/OneDrive/Bureaublad/Project2/2019/flightlist_20190101_20190131.csv"  
flightsDir = "C:/Users/TeleT/Downloads/Flight Data/2019/flightlist_20190101_20190131.csv"   # Tiago
airportDir = "Airports.csv"     # .CSV containing list of EU airports
cargoDir = "Cargo.csv"          # .CSV containing list of cargo airlines

# Define output file names (Change month and year of outputfile name accordingly)
europeanFlightsDir = "EU_flights_2019_01.csv"       # .CSV containing list of European flights
interFlightsDir = "Inter_flights_2019_01.csv"       # .CSV containing list of intercontinental flights
sortedFlightsDir = "Sorted_flights_2019_01.csv"     # .CSV containing list of all valid flights
missingFlightsDir = "Missing_flights_2019_01.csv"   # .CSV cintaining list of all missing data

# Open files
flightsFile = open(flightsDir, encoding="utf8")
airportFile = open(assetDir + airportDir, encoding="utf8")
cargoFlights = open(assetDir + cargoDir, encoding="utf8")

# Read files
flightsCSV = csv.reader(flightsFile)
airportCSV = csv.reader(airportFile)
cargoCSV = csv.reader(cargoFlights)

# Convert flight database from .CSV to List
flightList = []
for flight in flightsCSV:
    del (flight[1:5])   # Remove items after Callsign and before Origin
    del (flight[3:12])  # Remove items after Destinations 
    flightList.append(flight)

del (flightList[0])     # Remove legend

# Convert airport codes from .CSV to List
airportList = []
for airport in airportCSV:
    airportList.append(airport[1])

del(airportList[0])             # Remove legend
airportSet = set(airportList)   # Convert to Set

# Convert cargo codes from .CSV to List
cargoList = []
for cargoCode in cargoCSV:
    for i in range(len(cargoCode)):
        cargoList.append(cargoCode[i])

cargoSet = set(cargoList)   # Convert to Set


print("Total number of flights before sorting: ", len(flightList), "\n")

## ---------- Filters ---------- ##
# Filter 1 - Check for Origin and Destination
resultList = []
missingList = []
for flight in flightList:
    if flight[1] != "" and flight[2] != "":
        resultList.append(flight)
    else:
        missingList.append(flight)

print("Filter 1:", len(flightList) - len(resultList), " flights had no origin or destination")
flightList = resultList     # Reset process


# Filter 2 - Check if airports are distinct and in Europe
resultList = []

for flight in flightList:
    if (flight[1] in airportSet or flight[2] in airportSet) and (flight[1] != flight[2]):
        resultList.append(flight)

print("Filter 2:", len(flightList) - len(resultList), " flights had no airport in Europe")
flightList = resultList     # Reset process


# Filter 3 - Check if not military
resultList = []

for flight in flightList:
    if isMilitaryInEu(flight[1], ['B', 'E', 'L'], airportSet) == False \
        and isMilitaryInEu(flight[2], ['B', 'E', 'L'], airportSet) == False:
            resultList.append(flight)

print("Filter 3:", len(flightList) - len(resultList), " flights were from a military base in europe")
flightList = resultList     # Reset process


# Filter 4 - Check if Origin or Destination contain a number (American airfields)
resultList = []

for flight in flightList:
    if containsNumber(flight[1]) == False and containsNumber(flight[2]) == False:
        resultList.append(flight)

print("Filter 4:", len(flightList) - len(resultList), " flights had a number in the origin or destination")
flightList = resultList     # Reset process


# Filter 5 - Check if flight is from a cargo airline
resultList = []

for flight in flightList:

    if flight[0][0:3] not in cargoSet:
        resultList.append(flight)

print("Filter 5:", len(flightList) - len(resultList), " flights were from a cargo airline\n")
flightList = resultList     # Reset process


## ---------- Exporting ---------- ##

print("Total number of flights after sorting: ", len(flightList))
print("Runtime of all filters:", round(time.time() - startTime, 1) , "s\n")

euFlightList = []
interFlightList = []

for flight in flightList:
    if flight[1] in airportSet and flight[2] in airportSet:
        euFlightList.append(flight)
    else:
        interFlightList.append(flight)

# Create .CSV with European flights
with open(dir2019 + europeanFlightsDir , 'w') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(["Callsign", " Origin", " Destination"])
    for row in euFlightList:
        thewriter.writerow(row)

# Create .CSV with intercontinental flights
with open(dir2019 + interFlightsDir , 'w') as g:
    thewriter = csv.writer(g)
    thewriter.writerow(["Callsign", " Origin", " Destination"])
    for row in interFlightList:
        thewriter.writerow(row)

# Create .CSV with all filtered flights
with open(dir2019 + sortedFlightsDir , 'w') as h:
    thewriter = csv.writer(h)
    thewriter.writerow(["Callsign", " Origin", " Destination"])
    for row in flightList:
        thewriter.writerow(row)

# Create .CSV with all missing flights
with open(misDir + missingFlightsDir , 'w') as h:
    thewriter = csv.writer(h)
    thewriter.writerow(["Callsign", " Origin", " Destination"])
    for row in missingList:
        thewriter.writerow(row)

# Print information about exported files
print("Exported a file with " + str(len(euFlightList)) + " entries in \"" + dir2019 + europeanFlightsDir + "\"")
print("Exported a file with " + str(len(interFlightList)) + " entries in \"" + dir2019 + interFlightsDir + "\"")
print("Exported a file with " + str(len(flightList)) + " entries in \"" + dir2019 + sortedFlightsDir + "\"")
print("Exported a file with " + str(len(missingList)) + " entries in \"" + misDir + missingFlightsDir + "\"\n")
