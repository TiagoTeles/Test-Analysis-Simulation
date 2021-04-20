import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import csv

# Get dataset
# Make sure data is in array with shape (xxx,2)
GITDIR = __file__[0:-6]

Data = open(GITDIR + 'RNAF_Fleet.csv', encoding="utf8")
data_csv = csv.reader(Data)

Datapoints = []
Raw = []
Raw_1 = []
results = []
results_1 =[]
results_2 = []

for i in data_csv:
    Datapoints.append(i)
del Datapoints[0] # Remove legend

for i in range(len(Datapoints)):
    Raw.append(Datapoints[i][1:-1])
    results.append(Datapoints[i][-1])
print(np.array(Datapoints))

for i in Raw:
    for j in range(4):
        i[j] = float(i[j])

for i in range(len(results)):
    results[i] = float(results[i])

filtered_data = []

# Pre-selected cluster centers based on k-means method
index = [2,9]
inverse = [0,1,3,4,5,6,7,8,10,11,12,13]

for i in index:
    filtered_data.append(Raw[i])
    results_1.append(results[i])

for i in inverse:
    Raw_1.append(Raw[i])
    results_2.append(results[i])
# Make arrays
np.array(filtered_data), np.array(Raw_1), np.array(results)
np.array(results_1), np.array(results_2)
print('\n', filtered_data), print(Raw_1)

# Make model and compare with training data
clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
clf.fit(filtered_data, results_1)
y_svm = clf.predict(Raw_1)
print('\n', y_svm)