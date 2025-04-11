import numpy as np
import pandas as pd
from data.data_loader import DataLoader


def process_daily_data(lsmdf, lsmc, wind_speed_daily, wind_capacity_factor_daily, save=False):

    # input data has daily granularity, compute mean
    avg_wind_speed = np.mean(wind_speed_daily, axis=0)
    avg_capacity_factor = np.mean(wind_capacity_factor_daily, axis=0)

    lon = lsmdf.longitude.values  # shape (166,)
    lat = lsmdf.latitude.values   # shape (134,)

    lon_grid, lat_grid = np.meshgrid(lon, lat)

    flat_lon = lon_grid.flatten()
    flat_lat = lat_grid.flatten()
    flat_avg_wind_speed = avg_wind_speed.flatten()
    flat_avg_capacity_factor = avg_capacity_factor.flatten()
    flat_lsmc = lsmc.flatten()

    # filter: keep only land cells
    land_mask = flat_lsmc == 1

    flat_lon = flat_lon[land_mask]
    flat_lat = flat_lat[land_mask]
    flat_avg_wind_speed = flat_avg_wind_speed[land_mask]
    flat_avg_capacity_factor = flat_avg_capacity_factor[land_mask]

    df_wind_speed = pd.DataFrame({
        "Longitude": flat_lon,
        "Latitude": flat_lat,
        "avg_wind_speed": flat_avg_wind_speed
    })

    df_capacity_factor = pd.DataFrame({
        "Longitude": flat_lon,
        "Latitude": flat_lat,
        "avg_capacity_factor": flat_avg_capacity_factor
    })

    print(df_wind_speed.head(3))
    print(df_capacity_factor.head(3))
    print(f"Shape of capacity factor df: {df_capacity_factor.shape}")
    print(f"Shape of wind speed df: {df_wind_speed.shape}")

    if save:
        df_wind_speed.to_csv(f"{output_data_folder}/avg_wind_speed.csv", index=False)
        df_capacity_factor.to_csv(f"{output_data_folder}/avg_capacity_factor.csv", index=False)

if __name__ == "__main__":
    input_data_folder = "../data/raw"
    output_data_folder = "../data/basetables"
    data_loader = DataLoader(input_data_folder)
    lsmdf, lsmc, wind_speed_daily, wind_capacity_factor_daily = data_loader.load_wind_speed_data()
    process_daily_data(lsmdf, lsmc, wind_speed_daily,
                       wind_capacity_factor_daily, save=True)
