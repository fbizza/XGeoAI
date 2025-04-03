import numpy as np
import pandas as pd

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

    def get_correlation_values(self, target_coords):
        """Get the mean of correlation values for multiple target locations."""
        correlation_values = np.zeros((len(self.land_coords[0]), len(target_coords)))

        for i, (lat, lon) in enumerate(target_coords):
            land_index, _, _ = self.find_closest_land_point(lat, lon)
            if land_index is None:
                return None
            correlation_values[:, i] = self.correlation_matrix[land_index, :]

        return np.mean(correlation_values, axis=1)

    @staticmethod
    def get_correlation_df(latitude, longitude, land_coords, correlation_values):
        df = pd.DataFrame({
            'Latitude': latitude[land_coords[0]],
            'Longitude': longitude[land_coords[1]],
            'Mean Correlation': correlation_values
        })
        return df