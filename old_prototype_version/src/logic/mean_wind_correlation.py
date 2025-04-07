import numpy as np
import pickle
import pandas as pd
import os

def process_and_save_df():
    """Loads data, calculates mean correlations, and saves to a CSV with lon and lat"""
    data_folder = '../../data/raw/'
    output_filepath = '../../data/basetables/mean_wind_correlation_df'

    with open(os.path.join(data_folder, 'aus_region_mask.pkl'), 'rb') as f:
        lsmdf = pickle.load(f)
    with open(os.path.join(data_folder, 'aus_region_mask_lsmc.pkl'), 'rb') as f:
        lsmc = pickle.load(f)
    with open(os.path.join(data_folder, 'wind_correlation_matrix.pkl'), 'rb') as f:
        rlsmcs5Wmnavg = pickle.load(f)

    mean_correlations = np.mean(rlsmcs5Wmnavg, axis=1)
    mean_correlation_map = np.empty(np.shape(lsmc)) * np.nan
    land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)
    land_coords = np.unravel_index(land_indices.flatten(), np.shape(lsmc))
    mean_correlation_map[land_coords] = mean_correlations

    longitude = lsmdf.longitude.values
    latitude = lsmdf.latitude.values

    mean_correlations_flat = np.ndarray.flatten(mean_correlation_map)
    mean_correlations_land = mean_correlations_flat[land_indices.flatten()]

    df = pd.DataFrame({
        'Latitude': latitude[land_coords[0]],
        'Longitude': longitude[land_coords[1]],
        'Mean Correlation': mean_correlations_land
    })

    df.to_csv(output_filepath, index=False)
    print(f"DataFrame saved to: {output_filepath}")

if __name__ == "__main__":
    process_and_save_df()

