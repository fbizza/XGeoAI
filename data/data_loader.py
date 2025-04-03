import pickle
import pandas as pd

class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_pickle(self, filename):
        """Load a pickle file."""
        with open(f"{self.data_path}/{filename}", "rb") as f:
            return pickle.load(f)

    def load_csv(self, file_path):
        """Load a CSV file."""
        return pd.read_csv(file_path)

    def load_wind_data(self):
        """Load all required wind datasets."""
        lsmdf = self.load_pickle("aus_region_mask.pkl")
        lsmc = self.load_pickle("aus_region_mask_lsmc.pkl")
        rlsmcs5Wmnavg = self.load_pickle("wind_correlation_matrix.pkl")
        return lsmdf, lsmc, rlsmcs5Wmnavg