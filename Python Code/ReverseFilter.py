# = = = = = = = = = = #
#  Reverse Filter v1  #
# = = = = = = = = = = #


# == Set-up == #

filename1 = 'FebruaryInput'     # Input filename
filename2 = 'You_Should_Change_This'    # Output filename

import csv
f = open(filename1 + '.csv')
csv_f = csv.reader(f)
print("Filtering '" + filename1 + "'\n")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



# == Filter 1 a == #  
# Split the data into full rows and incomplete rows

rows, n1, t = [], 0, 0
incomplete_rows, full_rows = [], []
for row in csv_f:
    t = t + 1
    rows.append(row)
    if row[5] != "" and row[6] != "":
        full_rows.append(row)
    else:
        n1 = n1 + 1
        incomplete_rows.append(row)
    del(row[0:5])
    del(row[2:11]) 

del(rows[0]) # Deletes the first line
print("Filter 1a: " + str(n1) + " out of " + str(t) + " lines do not contain origin and/or destination")

# == Filter 1 b == #
# Deletes the 'empty' rows, which contain nether origin nor destination

faulty, g = [], 0
half_rows, half_rows1, half_rows2 = [], [], []
for i in range(len(incomplete_rows)):
    if incomplete_rows[i][0] == "" and incomplete_rows[i][1] == "":
        faulty.append(i)
        g += 1
    else:
        half_rows.append(incomplete_rows[i])
print("Filter 1b: " + str(g) + " out of " + str(n1) + " lines contain neither origin nor destination and were deleted")
print("\nSo " + str(len(half_rows)) + " lines are only half complete, and will be further analyzed")
"""
faulty.reverse()
for entry in faulty:
    half_rows.pop(entry)
"""

# == Filter 1 c == #
# Split the half rows into two categories, based on which entry is absent

for i in range(len(half_rows)):
    if half_rows[i][0] == "":
        half_rows2.append(half_rows[i])
    else:
        half_rows1.append(half_rows[i])

# == Filter 2 == #
# Filters entries to start with E, B or L

u_rows1, c1 = [], 0
for i in range(len(half_rows1)):
    if half_rows1[i][0][0] == "E" or half_rows1[i][0][0] == "B" or half_rows1[i][0][0] == "L":
        c1 = c1 + 1
        u_rows1.append(half_rows1[i])

u_rows2, c2 = [], 0
for i in range(len(half_rows2)):
    if half_rows2[i][1][0] == "E" or half_rows2[i][1][0] == "B" or half_rows2[i][1][0] == "L":
        c2 = c2 + 1
        u_rows2.append(half_rows2[i])
perc = round((c1+c2)/len(half_rows)*100,2)
print("\nOut of the " + str(len(half_rows)) + " half complete lines, there are approximately " + str(c1 + c2) + " with either origin or destination within Europe, which corresponds to " + str(perc) + " percent")

