import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn.cluster import KMeans

# Get dataset
# Make sure data is in array with shape (xxx,2)
GITDIR = __file__[0:-21]

Data = open(GITDIR + 'RNAF_Fleet.csv', encoding="utf8")
data_csv = csv.reader(Data)

Datapoints = []
filtered_data = []
for i in data_csv:
    Datapoints.append(i)

del Datapoints[0] # Remove legend

for i in range(len(Datapoints)):
    filtered_data.append(Datapoints[i][1:3])

print(np.array(Datapoints))

for i in range(len(Datapoints)):
    Datapoints[i] = Datapoints[i][0]

for i in filtered_data:
    for j in range(2):
        i[j] = float(i[j])
Data_x = np.array(filtered_data)

# Create KMeans object
number = 6
kmeans = KMeans(n_clusters = number)
kmeans.fit(Data_x)
clusters = kmeans.cluster_centers_
y_km = kmeans.fit_predict(Data_x)

# Set up colours for plots
colours = ['salmon', 'dodgerblue', 'forestgreen', 'orange', 'blueviolet', 'khaki', 'black', 'purple']

# Make the plots
for i in range(len(clusters)):
    plt.scatter(Data_x[y_km == i, 0], Data_x[y_km == i, 1], s=20, color= colours[i])

# Set up empty cluster lists
l0 = []
l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []

indices = []
for i in y_km:
    indices.append(list(set(y_km)).index(i))

# Check what elements from indices correspond to the outcomes of cluster division
for i in range(len(Datapoints)):
    if indices[i] == 0:
        l0.append(Datapoints[i])
    if indices[i] == 1:
        l1.append(Datapoints[i])
    if indices[i] == 2:
        l2.append(Datapoints[i])
    if indices[i] == 3:
        l3.append(Datapoints[i])
    if indices[i] == 4:
        l4.append(Datapoints[i])
    if indices[i] == 5:
        l5.append(Datapoints[i])
    if indices[i] == 6:
        l6.append(Datapoints[i])

print('\n\n', l0), print(l1), print(l2), print(l3), print(l4), print(l5), print(l6)

plt.title('6 Group data division')
plt.xlabel('Vehicle length [m]')
plt.ylabel('Wingspan / rotor diameter [m]')
plt.show()