import numpy as np
import pandas as pd
import os
from sklearn.metrics import pairwise_distances
import pickle

def process_and_save_mean_distances():
    """Loads data, calculates mean Euclidean distances in correlation space, and saves to a CSV with lon and lat."""
    data_folder = '../../data/raw/'
    output_filepath = '../../data/basetables/mean_wind_correlation_distance_df'

    with open(os.path.join(data_folder, 'aus_region_mask.pkl'), 'rb') as f:
        lsmdf = pickle.load(f)
    with open(os.path.join(data_folder, 'aus_region_mask_lsmc.pkl'), 'rb') as f:
        lsmc = pickle.load(f)
    with open(os.path.join(data_folder, 'wind_correlation_matrix.pkl'), 'rb') as f:
        rlsmcs5Wmnavg = pickle.load(f)

    pdist = pairwise_distances(rlsmcs5Wmnavg)
    mean_distances = np.mean(pdist, axis=1)
    land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)
    land_coords = np.unravel_index(land_indices.flatten(), np.shape(lsmc))

    longitude = lsmdf.longitude.values
    latitude = lsmdf.latitude.values

    mean_distances_map_flat = np.full(lsmc.size, np.nan)
    mean_distances_map_flat[land_indices.flatten()] = mean_distances
    mean_distances_land = mean_distances_map_flat[land_indices.flatten()]

    df = pd.DataFrame({
        'Latitude': latitude[land_coords[0]],
        'Longitude': longitude[land_coords[1]],
        'Mean Distance': mean_distances_land
    })

    df.to_csv(output_filepath, index=False)
    print(f"DataFrame saved to: {output_filepath}")

if __name__ == "__main__":
    process_and_save_mean_distances()