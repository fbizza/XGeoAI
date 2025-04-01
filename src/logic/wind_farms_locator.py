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

    wind_farm_coords = wind_farm[['Latitude', 'Longitude']].values
    wind_farm_latitude, wind_farm_longitude = wind_farm_coords[0]

    land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)
    land_coords = np.unravel_index(land_indices.flatten(), np.shape(lsmc))

    longitude = lsmdf.longitude.values
    latitude = lsmdf.latitude.values

    land_df = pd.DataFrame({
        'Latitude': latitude[land_coords[0]],
        'Longitude': longitude[land_coords[1]]
    })

    land_coords = land_df[['Latitude', 'Longitude']].values
    distances = pairwise_distances(wind_farm_coords, land_coords)
    closest_idx = np.argmin(distances)

    closest_land = land_df.iloc[closest_idx]
    closest_latitude, closest_longitude = closest_land['Latitude'], closest_land['Longitude']

    return wind_farm_latitude, wind_farm_longitude, closest_latitude, closest_longitude


def find_operating_wind_farms_locations(wind_farms_df, lsmdf, lsmc):
    """Returns a DataFrame of operating wind farms with closest land location."""

    operating_wind_farms = wind_farms_df[wind_farms_df['Development Status'] == 'Operating']

    results = []

    for _, wind_farm in operating_wind_farms.iterrows():
        wind_farm_lat, wind_farm_lon, closest_lat, closest_lon = find_closest_land_location(wind_farms_df, wind_farm['Asset'],
                                                                                          lsmdf, lsmc)

        result = wind_farm.to_dict()
        result['Closest ERA5 Land Latitude'] = closest_lat
        result['Closest ERA5 Land Longitude'] = closest_lon
        results.append(result)

    result_df = pd.DataFrame(results)

    return result_df


if __name__ == "__main__":
    data_folder = '../../data/raw/'

    with open(os.path.join(data_folder, 'aus_region_mask.pkl'), 'rb') as f:
        lsmdf = pickle.load(f)
    with open(os.path.join(data_folder, 'aus_region_mask_lsmc.pkl'), 'rb') as f:
        lsmc = pickle.load(f)

    file_path = '../../data/processed/wind-farms.csv'
    wind_farms_df = pd.read_csv(file_path)

    operating_wind_farms_df = find_operating_wind_farms_locations(wind_farms_df, lsmdf, lsmc)

    print("\n--- Operating Wind Farms with Closest Land Location ---")
    pd.set_option('display.max_columns', None)
    print(operating_wind_farms_df.head())

    output_path = '../../data/processed/wind-farms-with-ERA5_coordinates.csv'
    operating_wind_farms_df.to_csv(output_path, index=False)
