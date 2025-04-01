import numpy as np
import pickle
import os

def process_and_save_df():
    """Loads data, calculates mean correlations, and saves to a CSV with lon and lat"""
    data_folder = '../../data/raw/'

    # Load the data
    with open(os.path.join(data_folder, 'aus_region_mask.pkl'), 'rb') as f:
        lsmdf = pickle.load(f)
    with open(os.path.join(data_folder, 'aus_region_mask_lsmc.pkl'), 'rb') as f:
        lsmc = pickle.load(f)
    with open(os.path.join(data_folder, 'wind_correlation_matrix.pkl'), 'rb') as f:
        rlsmcs5Wmnavg = pickle.load(f)

    # Calculate the mean correlation
    mean_correlations = np.mean(rlsmcs5Wmnavg, axis=1)

    # Create the map of correlations (initially with NaN)
    mean_correlation_map = np.empty(np.shape(lsmc)) * np.nan

    # Get indices of land points (where lsmc == 1)
    land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)
    land_coords = np.unravel_index(land_indices.flatten(), np.shape(lsmc))

    # Map the mean correlation values to the mean_correlation_map
    mean_correlation_map[land_coords] = mean_correlations

    # Longitude and Latitude from lsmdf
    longitude = lsmdf.longitude.values
    latitude = lsmdf.latitude.values

    # Define target coordinates for search
    target_latitude = -33.75  # Updated target latitude
    target_longitude = 150.0  # Target longitude

    # Find the closest latitude and longitude index in the array
    lat_idx = np.abs(latitude - target_latitude).argmin()
    lon_idx = np.abs(longitude - target_longitude).argmin()

    # Print the closest latitude and longitude index
    print(f"Closest latitude index: {lat_idx}, Closest longitude index: {lon_idx}")

    # Retrieve the mean correlation for this location
    correlation_value = mean_correlation_map[lat_idx, lon_idx]
    print(f"Mean correlation for latitude {target_latitude} and longitude {target_longitude}: {correlation_value}")

    # To debug, let's print a small neighborhood of values around the target index:
    neighborhood = mean_correlation_map[lat_idx-2:lat_idx+3, lon_idx-2:lon_idx+3]
    print(f"Neighborhood around target index ({lat_idx}, {lon_idx}):")
    print(neighborhood)


if __name__ == "__main__":
    process_and_save_df()
