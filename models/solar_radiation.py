import numpy as np
import pandas as pd
from data.data_loader import DataLoader


def process_daily_data(lsmdf, lsmc, solar_radiation_daily, save=False):

    # input data has daily granularity, compute mean
    avg_solar_radiation = np.mean(solar_radiation_daily, axis=0)

    lon = lsmdf.longitude.values  # shape (166,)
    lat = lsmdf.latitude.values   # shape (134,)

    lon_grid, lat_grid = np.meshgrid(lon, lat)

    flat_lon = lon_grid.flatten()
    flat_lat = lat_grid.flatten()
    flat_avg_solar_radiation = avg_solar_radiation.flatten()
    flat_lsmc = lsmc.flatten()

    # filter: keep only land cells
    land_mask = flat_lsmc == 1

    flat_lon = flat_lon[land_mask]
    flat_lat = flat_lat[land_mask]
    flat_avg_solar_radiation = flat_avg_solar_radiation[land_mask]

    df_solar_radiation = pd.DataFrame({
        "Longitude": flat_lon,
        "Latitude": flat_lat,
        "avg_solar_radiation": flat_avg_solar_radiation
    })

    print(df_solar_radiation.head(3))
    print(f"Shape of wind speed df: {df_solar_radiation.shape}")

    if save:
        df_solar_radiation.to_csv(f"{output_data_folder}/avg_solar_radiation.csv", index=False)

if __name__ == "__main__":
    input_data_folder = "../data/raw"
    output_data_folder = "../data/basetables"
    data_loader = DataLoader(input_data_folder)
    lsmdf, lsmc, solar_radiation_daily, _ = data_loader.load_solar_radiation_data()
    process_daily_data(lsmdf, lsmc, solar_radiation_daily, save=True)
