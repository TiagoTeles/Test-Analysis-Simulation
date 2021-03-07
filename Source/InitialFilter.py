# Imports
import csv

"""
This script filters out flights that do not belong in the data analysis. The
criteria for inclusion are the following:
- Has Origin or Destination
- Origin or Destination are in Europe (ICAO E, B or L) # Doesn't this make the first step obsolete?
- Origin or Destinations ICAO codes do not contain a number

The input .CSV file has the following structure:
Callsign, Flight Number, Transponder Code, A/C Registration, Type Code,
Origin, Destination, First Seen, Last Seen, Day, Latitude_1, Longitude_1,
Altitude_1, Latitude_2, Longitude_2, Altitude_2
"""

# Proposed Workflow:
# This Script:
# Remove unnecessary data
# Remove flights w/o origin and destination or numbers in ICAO code
# Set incomplete flights aside
# Remove non-european flights from complete flights
# Export complete.csv and incomplete.csv

# == Set-up == #
assetDir = __file__[0:-23] + "Assets/"
inputFile = "Unfiltered"  # Input filename
outputFile = "You_Should_Change_This"  # Output filename


f = open(assetDir + inputFile + '.csv')
csv_f = csv.reader(f)
print("Filtering '" + inputFile + "'\n")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# == Filter 1 == #
# Delete all lines without origin or destination
# Also delete all unnecessary information

rows, n1, t = [], 0, 0
for row in csv_f:
    t += 1
    if row[5] != "" and row[6] != "":
        rows.append(row)
    else:
        n1 = n1 + 1
    del (row[0:5])
    del (row[2:11])

del (rows[0])  # Deletes the first line
print("Filter 1: " + str(n1) + " out of " + str(t) + " lines are invalid and were deleted")

# == Filter 2 == #
# Delete all entries not starting with E, B or L

u_rows, n2 = [], 0
for i in range(len(rows)):
    if rows[i][0][0] == "E" or rows[i][0][0] == "B" or rows[i][0][0] == "L" \
            or rows[i][1][0] == "E" or rows[i][1][0] == "B" or rows[i][1][0] == "L":
        n2 = n2 + 1
        u_rows.append(rows[i])
print("Filter 2: " + str(n1 - n2) + " lines had no link to European airports and were deleted")

# == Filter 3 == #
# Delete all entries containing a number

faulty, n3 = [], 0
for i in range(len(u_rows)):
    if is_number(u_rows[i][1][2]) or is_number(u_rows[i][0][2]) or is_number(u_rows[i][1][0]) \
            or is_number(u_rows[i][0][0]) or is_number(u_rows[i][1][1]) or is_number(u_rows[i][0][1]) \
            or is_number(u_rows[i][1][3]) or is_number(u_rows[i][0][3]):
        n3 = n3 + 1
        faulty.append(i)

faulty.reverse()  # Might seem odd but this has an important reason, ask me if interested
for entry in faulty:
    u_rows.pop(entry)
print("Filter 3: " + str(n3) + " lines contain a number and were deleted")
print("\nFiltering complete")

# == Exporting == #
'''
with open(filename2 + '.csv', 'w') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(["source", "target"])
    for i in range(len(u_rows)):
        thewriter.writerow([rows[i][0], rows[i][1]])
print("Exported a file with " + str(len(u_rows)) + " entries called '" + filename2 + "'")
'''