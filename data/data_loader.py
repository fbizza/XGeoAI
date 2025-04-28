import pickle
import pandas as pd

class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_pickle(self, filename):
        with open(f"{self.data_path}/{filename}", "rb") as f:
            return pickle.load(f)

    def load_csv(self, file_path):
        #TODO: adjust, use data fodler and file name
        return pd.read_csv(file_path)

    def load_wind_correlation_data(self):
        lsmdf = self.load_pickle("aus_region_mask.pkl")
        lsmc = self.load_pickle("aus_region_mask_lsmc.pkl")
        rlsmcs5Wmnavg = self.load_pickle("wind_correlation_matrix.pkl")
        return lsmdf, lsmc, rlsmcs5Wmnavg

    def load_wind_speed_data(self):
        lsmdf = self.load_pickle("aus_region_mask.pkl")
        lsmc = self.load_pickle("aus_region_mask_lsmc.pkl")
        wind_speed_daily = self.load_pickle("wind_speed_daily.pkl")
        wind_capacity_factor_daily = self.load_pickle("wind_capacity_factor_daily.pkl")
        return lsmdf, lsmc, wind_speed_daily, wind_capacity_factor_daily

    def load_solar_radiation_data(self):
        lsmdf = self.load_pickle("aus_region_mask.pkl")
        lsmc = self.load_pickle("aus_region_mask_lsmc.pkl")
        solar_radiation_daily = self.load_pickle("solar_radiation_daily.pkl")
        solar_correlation_matrix = self.load_pickle("solar_correlation_matrix.pkl")
        return lsmdf, lsmc, solar_radiation_daily, solar_correlation_matrix
