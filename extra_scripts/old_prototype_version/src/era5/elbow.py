import numpy as np
import xarray as xr
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import squareform
import pickle
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch

with open('../../../../data/raw/aus_region_mask.pkl', 'rb') as f:
    lsmdf = pickle.load(f)
with open('../../../../data/raw/aus_region_mask_lsmc.pkl', 'rb') as f:
    lsmc = pickle.load(f)
with open('../../../../data/raw/wind_correlation_matrix.pkl', 'rb') as f:
    rlsmcs5Wmnavg = pickle.load(f)

pdist = pairwise_distances(rlsmcs5Wmnavg)
linkage = sch.linkage(squareform(pdist.astype('float32')), method='complete')
ninds0 = 15 #hard code
idx = sch.fcluster(linkage, ninds0, 'maxclust')
idxmap = np.empty((np.shape(lsmc)[0]*np.shape(lsmc)[1]))*np.nan
inds = np.ndarray.flatten(np.argwhere(np.ndarray.flatten(lsmc)==1))
idxmap[inds] = idx
idxmap = idxmap.reshape(np.shape(lsmc)[0],np.shape(lsmc)[1])

from sklearn.cluster import KMeans
from tqdm import tqdm  # Import tqdm for the progress bar




# List to store inertia values
inertia_values = []

# Range of clusters to try (e.g., from 1 to 20 clusters)
cluster_range = range(1, 31)

# Iterate through different cluster sizes using tqdm to show progress
for n_clusters in tqdm(cluster_range, desc="K-means clustering", unit="cluster"):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(pdist)  # Fit KMeans on the data
    inertia_values.append(kmeans.inertia_)  # Append the inertia (sum of squared distances)

# Plot the elbow method
plt.figure(figsize=(8, 6))
plt.plot(cluster_range, inertia_values, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia (Sum of Squared Distances)')
plt.xticks(range(1, 31))
plt.show()