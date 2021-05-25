import csv


flight_file = open('C:/Users/mathi/OneDrive/Documenten/GitHub/Test-Analysis-Simulation/Missing_Flights/Missing_flights_2019_01.csv', encoding="utf8")
airport_file = open('C:/Users/mathi/OneDrive/Documenten/GitHub/Test-Analysis-Simulation/Assets/Airports.csv', encoding="utf8")
cargo_file = open('C:/Users/mathi/OneDrive/Documenten/GitHub/Test-Analysis-Simulation/Assets/Cargo.csv', encoding="utf8")

flight_csv = csv.reader(flight_file)
airport_csv = csv.reader(airport_file)
cargo_csv = csv.reader(cargo_file)


# Convert flight database from .CSV to List
flight_list = []
for flight in flight_csv:
    if flight != []:
        flight_list.append(flight)

del flight_list[0]       # Remove legend


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


#Filter 2 - Check if airports are distinct and in Europe
result_list = []

for flight in flight_list:
    if (flight[1] in airportSet or flight[2] in airportSet) and (flight[1] != flight[2]):
        result_list.append(flight)

print("Filter 2:", len(flight_list) - len(result_list), " flights had no airport in Europe")
flight_list = result_list     # Reset process


# Filter 3 - Check if flight is from a cargo airline
result_list = []

for flight in flight_list:

    if flight[0][0:3] not in cargoSet:
        result_list.append(flight)

print("Filter 5:", len(flight_list) - len(result_list), " flights were from a cargo airline\n")
flight_list = result_list     # Reset process

print("\nNumber of incomplete flights with Origin/Destination in Europe:", len(flight_list))
