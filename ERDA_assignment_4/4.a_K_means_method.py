import time

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets import make_blobs

# #############################################################################
# Generate sample data
np.random.seed(0)

batch_size = 45
centers = [[1, 1], [-1, -1], [1, -1]]
n_clusters = len(centers)
X, labels_true = make_blobs(n_samples=3000, centers=centers, cluster_std=0.5)

# #############################################################################
# Compute clustering with Means

k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
t0 = time.time()
k_means.fit(X)
t_batch = time.time() - t0

# #############################################################################
# Plot result

fig = plt.figure(figsize=(8, 3))
colors = ['r', 'b', 'y', 'orange']

# We want to have the same colors for the same cluster from the
# MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
# closest one.
k_means_cluster_centers = k_means.cluster_centers_

k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)

# KMeans
for k, col in zip(range(n_clusters), colors):
    my_members = k_means_labels == k
    cluster_center = k_means_cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], 'w',
            markerfacecolor=col, marker='.', alpha = 0.5)
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=6)
plt.title('KMeans')
plt.xticks(())
plt.yticks(())
plt.show()



# # Set colours
# colours = {'b','g','r','orange','m','y','brown'}
#
# # Set or import data
# X = -2 * np.random.rand(100, 2)
# X1 = 1 + 2 * np.random.rand(50, 2)
# X[50:100, :] = X1
# plt.scatter(X[:, 0], X[:, 1], s=50, c='b')
# plt.show()
#
# # Run the k-means algorithm
# # Set the desired number of clusters
# clusters = 2
# kmeans = KMeans(n_clusters=clusters)
#
# kmeans.fit(X)
#
# centers = k_means.cluster_centers_
#
# labels = kmeans.predict(X)
#
#
# # Plot the data and clusters
#
# for k, col in zip(range(clusters), colours):
#     my_members = k_means_labels == k
#     cluster_center = kmeans_cluster_centers[k]
#     plt.plot(X[my_members, 0], X[my_members, 1], 'w',
#             markerfacecolor=col, marker='.')
#     ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
#             markeredgecolor='k', markersize=6)
# plt.scatter(X[:, 0], X[:, 1], alpha = 0.5, edgecolor = 'k')
# #plt.scatter()
# plt.show()
