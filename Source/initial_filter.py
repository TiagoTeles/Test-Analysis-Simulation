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


# ---------- Imports ---------- #
import csv
import time


# ---------- Function definitions ---------- #
def contains_number(string):
    """ Checks if input contains a number

    Arguments:
        s {String} -- Argument to be checked

    Returns:
        Boolean -- True if value contains a number
    """

    for character in string:
        try:
            float(character)
            return True
        except ValueError:
            pass

    return False


def is_military_eu(icao_code, letter_set, airport_database):
    """ Checks if ICAO code is from an European military airport

    Arguments:
        icaoCode {String} -- ICAO code of the airport to be checked
        letterSet {List} -- First letter of the airports to consider
        airportDatabase {List} -- List of civilian airports

    Returns:
        Boolean -- True if the airport is military and in Europe
    """

    return (icao_code[0] in letter_set) and (icao_code not in airport_database)


# ---------- Main Program ---------- #
start_time = time.time()

# Define directories
GIT_DIR = __file__[0:-24]
ASSET_DIR = GIT_DIR + "Assets/"
DIR_2019 = GIT_DIR + "2019_Filtered/"
DIR_2020 = GIT_DIR + "2020_Filtered/"
MIS_DIR = GIT_DIR + "Missing_Flights/"

# Define input file names
FLIGHT_DIR = "C:/Users/mathi/OneDrive/Bureaublad/Project2/2019/flightlist_20190101_20190131.csv"
# FLIGHT_DIR = "C:/Users/TeleT/Downloads/Flight Data/2019/flightlist_20190101_20190131.csv"   # Tiago
AIRPORT_DIR = "Airports.csv"     # .CSV containing list of EU airports
CARGO_DIR = "Cargo.csv"          # .CSV containing list of cargo airlines

# Define output file names (Change month and year of outputfile name)
EUROPEAN_FLIGHT_DIR = "EU_flights_2019_01.csv"
INTER_FLIGHT_DIR = "Inter_flights_2019_01.csv"
SORTED_FLIGHT_DIR = "Sorted_flights_2019_01.csv"
MISSING_FLIGHT_DIR = "Missing_flights_2019_01.csv"

# Open files
flight_file = open(FLIGHT_DIR, encoding="utf8")
airport_file = open(ASSET_DIR + AIRPORT_DIR, encoding="utf8")
cargo_file = open(ASSET_DIR + CARGO_DIR, encoding="utf8")

# Read files
flight_csv = csv.reader(flight_file)
airport_csv = csv.reader(airport_file)
cargo_csv = csv.reader(cargo_file)

# Convert flight database from .CSV to List
flight_list = []
for flight in flight_csv:
    del flight[1:5]     # Remove items after Callsign and before Origin
    del flight[3:5]     # Remove items between Destination and Day
    del flight[4:12]    # Remove items after Day
    flight_list.append(flight)

del flight_list[0]       # Remove legend

for row in flight_list:
    row[3] = row[3][0:11]

# Convert airport codes from .CSV to List
airport_list = []
for airport in airport_csv:
    airport_list.append(airport[1])

del airport_list[0]              # Remove legend
airportSet = set(airport_list)   # Convert to Set

# Convert cargo codes from .CSV to List
cargoList = []
for cargoCode in cargo_csv:
    for i in range(len(cargoCode)):
        cargoList.append(cargoCode[i])

cargoSet = set(cargoList)   # Convert to Set

print("Total number of flights before sorting: ", len(flight_list), "\n")


# ---------- Filters ---------- #
# Filter 1 - Check for Origin and Destination
result_list = []
missing_list = []
for flight in flight_list:
    if flight[1] != "" and flight[2] != "":
        result_list.append(flight)
    else:
        missing_list.append(flight)

print("Filter 1:", len(flight_list) - len(result_list), " flights had no origin or destination")
flight_list = result_list     # Reset process


# Filter 2 - Check if airports are distinct and in Europe
result_list = []

for flight in flight_list:
    if (flight[1] in airportSet or flight[2] in airportSet) and (flight[1] != flight[2]):
        result_list.append(flight)

print("Filter 2:", len(flight_list) - len(result_list), " flights had no airport in Europe")
flight_list = result_list     # Reset process


# Filter 3 - Check if not military
result_list = []

for flight in flight_list:
    if (is_military_eu(flight[1], ['B', 'E', 'L'], airportSet) is False and
            is_military_eu(flight[2], ['B', 'E', 'L'], airportSet) is False):
        result_list.append(flight)

print("Filter 3:", len(flight_list) - len(result_list), " flights were from a military base in europe")
flight_list = result_list     # Reset process


# Filter 4 - Check if Origin or Destination contain a number
result_list = []

for flight in flight_list:
    if contains_number(flight[1]) is False and contains_number(flight[2]) is False:
        result_list.append(flight)

print("Filter 4:", len(flight_list) - len(result_list), " flights had a number in the origin or destination")
flight_list = result_list     # Reset process


# Filter 5 - Check if flight is from a cargo airline
result_list = []

for flight in flight_list:

    if flight[0][0:3] not in cargoSet:
        result_list.append(flight)

print("Filter 5:", len(flight_list) - len(result_list), " flights were from a cargo airline\n")
flight_list = result_list     # Reset process


# ---------- Exporting ---------- #
print("Total number of flights after sorting: ", len(flight_list))
print("Runtime of all filters:", round(time.time() - start_time, 1), "s\n")

eu_flight_list = []
inter_flight_list = []

for flight in flight_list:
    if flight[1] in airportSet and flight[2] in airportSet:
        eu_flight_list.append(flight)
    else:
        inter_flight_list.append(flight)

# Create .CSV with European flights
with open(DIR_2019 + EUROPEAN_FLIGHT_DIR, 'w', newline="") as f:
    the_writer = csv.writer(f)
    the_writer.writerow(["Callsign", " Origin", " Destination", "Day"])
    for row in eu_flight_list:
        the_writer.writerow(row)

# Create .CSV with intercontinental flights
with open(DIR_2019 + INTER_FLIGHT_DIR, 'w', newline="") as g:
    the_writer = csv.writer(g)
    the_writer.writerow(["Callsign", " Origin", " Destination", "Day"])
    for row in inter_flight_list:
        the_writer.writerow(row)

# Create .CSV with all filtered flights
with open(DIR_2019 + SORTED_FLIGHT_DIR, 'w', newline="") as h:
    the_writer = csv.writer(h)
    the_writer.writerow(["Callsign", " Origin", " Destination", "Day"])
    for row in flight_list:
        the_writer.writerow(row)

# Create .CSV with all missing flights
with open(MIS_DIR + MISSING_FLIGHT_DIR, 'w', newline="") as h:
    the_writer = csv.writer(h)
    the_writer.writerow(["Callsign", " Origin", " Destination", "Day"])
    for row in missing_list:
        the_writer.writerow(row)

# Print information about exported files
print("Exported a file with " + str(len(eu_flight_list)) + " entries in \"" + DIR_2019 + EUROPEAN_FLIGHT_DIR + "\"")
print("Exported a file with " + str(len(inter_flight_list)) + " entries in \"" + DIR_2019 + INTER_FLIGHT_DIR + "\"")
print("Exported a file with " + str(len(flight_list)) + " entries in \"" + DIR_2019 + SORTED_FLIGHT_DIR + "\"")
print("Exported a file with " + str(len(missing_list)) + " entries in \"" + DIR_2019 + MISSING_FLIGHT_DIR + "\"\n")
