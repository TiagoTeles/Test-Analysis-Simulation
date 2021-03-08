import numpy as np
import csv
import time

#get file directories
f1 = 'C:/Users/mathi/OneDrive/Bureaublad/Project2/2019/flightlist_20190101_20190131' #input filename
f2 = 'C:/Users/mathi/OneDrive/Documenten/GitHub/Test-Analysis-Simulation/Assets/Cargo' #cargo icao airlines list


#open files
f_1 = open(f1 + '.csv')
csv_f = csv.reader(f_1)

f_2 = open(f2 + '.csv')
csv_f2 = csv.reader(f_2)

#print(f_2)

lines = []
#get list of airliners code
cargo = []
for row in csv_f2:
    for i in range(len(row)):
        cargo.append(row[i])

print(cargo)


#set counters
start = time.time()
number = 0
deleted = 0

for row in csv_f:
    lines.append(row)

    for code in cargo:
        
        #check if airliner codes match
        if row[0][0:3] == code:
            #delete entry 
            lines.remove(row)

            #count deleted
            deleted = deleted + 1
        else:
            continue
    #Keep total number of flights counter up to date
    number = number +1
    
#Testing the code
##    if number%10 ==0:
##        print(number)


#Maximum iteration number for testing
    if number == 15000:
        break
    
end = time.time()

print(deleted, ' cargo flights deleted out of ',number,' total evaluated.')
#print(lines)

print('Runtime for cargo filter = ',end-start)
