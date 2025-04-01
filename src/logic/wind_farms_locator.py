import numpy as np
import pandas as pd
import os
from sklearn.metrics import pairwise_distances
import pickle


def find_closest_land_location(wind_farms_df, asset_name, lsmdf, lsmc):
    """Finds the closest land location to a given wind farm asset"""
    wind_farm = wind_farms_df[wind_farms_df['Asset'] == asset_name]
    if wind_farm.empty:
        print("Asset not found.")
        return None

    wind_coords = wind_farm[['Latitude', 'Longitude']].values
    wind_latitude, wind_longitude = wind_coords[0]

    land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)
    land_coords = np.unravel_index(land_indices.flatten(), np.shape(lsmc))

    longitude = lsmdf.longitude.values
    latitude = lsmdf.latitude.values

    land_df = pd.DataFrame({
        'Latitude': latitude[land_coords[0]],
        'Longitude': longitude[land_coords[1]]
    })

    land_coords = land_df[['Latitude', 'Longitude']].values
    distances = pairwise_distances(wind_coords, land_coords)
    closest_idx = np.argmin(distances)

    closest_land = land_df.iloc[closest_idx]
    closest_latitude, closest_longitude = closest_land['Latitude'], closest_land['Longitude']

    # Improved print statements
    print("\n--- Wind Farm Information ---")
    print(f"Asset: {asset_name}")
    print(f"Latitude: {wind_latitude:.4f}")
    print(f"Longitude: {wind_longitude:.4f}")

    print("\n--- Closest Land Location ---")
    print(f"Latitude: {closest_latitude:.4f}")
    print(f"Longitude: {closest_longitude:.4f}")

    return closest_land


if __name__ == "__main__":
    data_folder = '../../data/raw/'

    with open(os.path.join(data_folder, 'aus_region_mask.pkl'), 'rb') as f:
        lsmdf = pickle.load(f)
    with open(os.path.join(data_folder, 'aus_region_mask_lsmc.pkl'), 'rb') as f:
        lsmc = pickle.load(f)

    file_path = '../../data/processed/wind-farms.csv'
    wind_farms_df = pd.read_csv(file_path)

    asset_name = "Hampton"
    closest_land_location = find_closest_land_location(wind_farms_df, asset_name, lsmdf, lsmc)
