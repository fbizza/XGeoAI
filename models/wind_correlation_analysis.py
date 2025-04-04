import numpy as np
import pandas as pd
import os
import pickle

class WindAnalyzer:
    def __init__(self, lsmdf, lsmc, correlation_matrix):
        self.lsmdf = lsmdf
        self.lsmc = lsmc
        self.correlation_matrix = correlation_matrix
        self.land_indices = np.argwhere(np.ndarray.flatten(self.lsmc) == 1)
        self.land_coords = np.unravel_index(self.land_indices.flatten(), self.lsmc.shape)
        self.latitude = self.lsmdf.latitude.values
        self.longitude = self.lsmdf.longitude.values

    def find_closest_land_point(self, target_lat, target_lon):
        """Find the closest land point to given coordinates."""
        lat_index = np.argmin(np.abs(self.latitude - target_lat))
        lon_index = np.argmin(np.abs(self.longitude - target_lon))

        land_index = np.where((self.land_coords[0] == lat_index) & (self.land_coords[1] == lon_index))[0]
        if len(land_index) == 0:
            return None  # No land found
        return land_index[0], self.latitude[lat_index], self.longitude[lon_index]

    def compute_mean_correlation(self, target_coords=None):
        """
        Extract the mean wind correlations for inland Australian locations.
        If target_coords is provided, it computes the mean correlation with those specific locations.
        If target_coords is None, it computes the mean correlation for all locations.
        """
        if target_coords is None:
            return np.mean(self.correlation_matrix, axis=1)  # Global mean correlation

        correlation_values = np.zeros((len(self.land_coords[0]), len(target_coords)))

        for i, (lat, lon) in enumerate(target_coords):
            land_index, _, _ = self.find_closest_land_point(lat, lon)
            if land_index is None:
                return None
            correlation_values[:, i] = self.correlation_matrix[land_index, :]

        return np.mean(correlation_values, axis=1)

    @staticmethod
    def build_correlation_df(latitude, longitude, land_coords, correlation_values):
        df = pd.DataFrame({
            'Latitude': latitude[land_coords[0]],
            'Longitude': longitude[land_coords[1]],
            'Mean Correlation': correlation_values
        })
        return df

    def save_correlation(self, data_folder, target_coords=None):
        """
        Computes and saves the mean correlation. If target_coords is provided, computes
        correlation for those targets, otherwise computes for the full dataset.

        The output file is saved in `data_folder`:
        - `all_locations_mean_correlation.csv` for global analysis.
        - `target_mean_correlation.csv` for target-specific analysis.
        """
        mean_correlations = self.compute_mean_correlation(target_coords)

        filename = "target_mean_correlation.csv" if target_coords else "all_locations_mean_correlation.csv"
        output_filepath = os.path.join(data_folder, filename)

        df = self.build_correlation_df(self.latitude, self.longitude, self.land_coords, mean_correlations)

        df.to_csv(output_filepath, index=False)

