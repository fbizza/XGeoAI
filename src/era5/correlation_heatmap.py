import numpy as np
import xarray as xr
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import squareform
import pickle
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
with open('../../data/raw/aus_region_mask.pkl','rb') as f:
    lsmdf = pickle.load(f)
with open('../../data/raw/aus_region_mask_lsmc.pkl','rb') as f:
    lsmc = pickle.load(f)
with open('../../data/raw/wind_correlation_matrix.pkl','rb') as f:
    rlsmcs5Wmnavg = pickle.load(f)

pdist = pairwise_distances(rlsmcs5Wmnavg)
#linkage = sch.linkage(squareform(pdist.astype('float32')), method='complete')
#ninds0 = 15 #hard code
#idx = sch.fcluster(linkage, ninds0, 'maxclust')
#idxmap = np.empty((np.shape(lsmc)[0]*np.shape(lsmc)[1]))*np.nan
#inds = np.ndarray.flatten(np.argwhere(np.ndarray.flatten(lsmc)==1))
#idxmap[inds] = idx
#idxmap = idxmap.reshape(np.shape(lsmc)[0],np.shape(lsmc)[1])


mean_distances = np.mean(pdist, axis=1)
mean_distance_map = np.empty(np.shape(lsmc)) * np.nan

land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)

# convert land indices to 2D (latitude, longitude) positions
# land_indices is a 2D array with indices of the land locations
land_coords = np.unravel_index(land_indices.flatten(), np.shape(lsmc))

mean_distance_map[land_coords] = mean_distances


plt.figure(figsize=(10, 8))
plt.pcolor(lsmdf.longitude, lsmdf.latitude, mean_distance_map, cmap='coolwarm')
#plt.colorbar(label='TODO: add proper label')
plt.title('Mean Euclidean distance in Correlation Space')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
