import csv
import time

# ---------- Main Program ---------- #
start_time = time.time()

# Define directories
GIT_DIR = __file__[0:-25]
ASSET_DIR = GIT_DIR + "Assets/"
DIR_2019 = GIT_DIR + "Combined_2019/"
DIR_2020 = GIT_DIR + "Combined_2020/"

# Define input file names
FLIGHT_DIR = DIR_2020 + 'Combined_2020_01.csv'
# FLIGHT_DIR = "C:/Users/TeleT/Downloads/Flight Data/2019/flightlist_20190101_20190131.csv"   # Tiago
AIRPORT_DIR = "Airports.csv"     # .CSV containing list of EU airports


# Open files
flight_file = open(FLIGHT_DIR, encoding="utf8")
airport_file = open(ASSET_DIR + AIRPORT_DIR, encoding="utf8")

# Read files
flight_csv = csv.reader(flight_file)
airport_csv = csv.reader(airport_file)

# Convert flight database from .CSV to List
flight_list = []
for flight in flight_csv:
    flight_list.append(flight)

del flight_list[0]       # Remove legend

# Convert airport codes from .CSV to List
airport_list = []
for airport in airport_csv:
    airport_list.append(airport[1])

del airport_list[0]              # Remove legend
airportSet = set(airport_list)   # Convert to Set

print("Total number of flights before sorting: ", len(flight_list), "\n")

# Filter 2 - Check if airports are distinct and in Europe
result_list = []
deleted = []
for flight in flight_list:
    if (flight[1] in airportSet and flight[2] in airportSet) and (flight[1] != flight[2]):
        result_list.append(flight)
    else:
        deleted.append(flight)

print("Filter 2:", len(flight_list) - len(result_list), " flights had no airport in Europe")
flight_list = result_list     # Reset process

# Create .CSV with European flights
with open(GIT_DIR + "Combined_2020_new/Combined_2020_01_b", 'w', newline="") as f:
    the_writer = csv.writer(f)
    the_writer.writerow(["Callsign", " Origin", " Destination", "Day"])
    for row in result_list:
        the_writer.writerow(row)
