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
FLIGHT_DIR = DIR_2019
# FLIGHT_DIR = "C:/Users/TeleT/Downloads/Flight Data/2019/flightlist_20190101_20190131.csv"   # Tiago
AIRPORT_DIR = "Airports.csv"     # .CSV containing list of EU airports

# Define output file names (Change month and year of outputfile name)
EUROPEAN_FLIGHT_DIR = "Combined_2019_01.csv"

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