import numpy as np
import csv
import gzip

#get file directories
f1 = 'C:/Users/mathi/OneDrive/Bureaublad/Project2/2019/flightlist_20190101_20190131' #input filename
f2 = 'C:/Users/mathi/OneDrive/Documenten/GitHub/Test-Analysis-Simulation/Assets/Cargo' #cargo icao airlines list


#open files
f_1 = open(f1 + '.csv')
csv_f = csv.reader(f_1)

f_2 = open(f2 + '.csv')
csv_f2 = csv.reader(f_2)

#print(f_2)


#get list of airliners code
cargo = []
for row in csv_f2:
    for i in range(len(row)):
        cargo.append(row[i])

print(cargo)


#set counters
number = 0
deleted = 0

test = 0
for row in csv_f:
    
    for code in cargo:
        
        #check if airliner codes match
        if row[0][0:3] == code:
            #delete entry still write


            #count deleted
            deleted = deleted + 1
        else:
            continue

    number = number +1
    test = test + 1

    if test == 1000:
        break

print(deleted)

