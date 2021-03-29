import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

# Get dataset
# Make sure data is in array with shape (xxx,2)
xy = np.random.uniform(-10.0, 10.0, size=(600, 2))

#Create KMeans object
kmeans = KMeans(n_clusters = 2)
kmeans.fit(xy)
clusters = kmeans.cluster_centers_

y_km = kmeans.fit_predict(xy)

# Set up colours for plots
colours = ['salmon', 'dodgerblue', 'forestgreen', 'orange', 'blueviolet', 'khaki']

# Make the plots
for i in range(len(clusters)):
    plt.scatter(xy[y_km == i, 0], xy[y_km == i, 1], s=20, color= colours[i])
for i in range(len(clusters)):
    plt.scatter(clusters[i][0], clusters[i][1], marker = '*', s = 100, color = 'black')

plt.show()
