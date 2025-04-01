import numpy as np
import pickle
import os

class WindCorrelationLookup:
    def __init__(self, data_folder='../../data/raw/'):
        """Loads data and prepares mean correlation map."""
        self.data_folder = data_folder
        self._load_data()
        self._compute_mean_correlation_map()

    def _load_data(self):
        """Loads required data from pickle files."""
        with open(os.path.join(self.data_folder, 'aus_region_mask.pkl'), 'rb') as f:
            self.lsmdf = pickle.load(f)
        with open(os.path.join(self.data_folder, 'aus_region_mask_lsmc.pkl'), 'rb') as f:
            self.lsmc = pickle.load(f)
        with open(os.path.join(self.data_folder, 'wind_correlation_matrix.pkl'), 'rb') as f:
            self.rlsmcs5Wmnavg = pickle.load(f)

        # Extract latitude and longitude from xarray dataset
        self.longitude = self.lsmdf.longitude.values
        self.latitude = self.lsmdf.latitude.values

    def _compute_mean_correlation_map(self):
        """Computes the mean correlation map for land points."""
        mean_correlations = np.mean(self.rlsmcs5Wmnavg, axis=1)

        # Initialize map with NaN values
        self.mean_correlation_map = np.full(self.lsmc.shape, np.nan)

        # Get land coordinates
        land_indices = np.argwhere(self.lsmc.flatten() == 1)
        land_coords = np.unravel_index(land_indices.flatten(), self.lsmc.shape)

        # Map mean correlations to the corresponding grid positions
        self.mean_correlation_map[land_coords] = mean_correlations

    def get_mean_correlation(self, latitude, longitude, mode="exact"):
        """
        Returns the mean correlation value for a given latitude and longitude.

        Parameters:
        - latitude (float): Latitude of the point.
        - longitude (float): Longitude of the point.
        - mode (str): "exact" (strict match) or "approx" (find nearest point).

        Returns:
        - float: Mean correlation value or None if not found (for "exact" mode).
        """
        if mode not in ["exact", "approx"]:
            raise ValueError("Mode must be 'exact' or 'approx'.")

        # Find closest indices
        lat_idx = np.where(self.latitude == latitude)[0]
        lon_idx = np.where(self.longitude == longitude)[0]

        # Exact mode: Return None if no exact match is found
        if mode == "exact":
            if len(lat_idx) == 0 or len(lon_idx) == 0:
                raise ValueError(f"No exact match found for ({latitude}, {longitude})")
            lat_idx, lon_idx = lat_idx[0], lon_idx[0]

        # Approximate mode: Find nearest latitude and longitude
        else:
            lat_idx = np.abs(self.latitude - latitude).argmin()
            lon_idx = np.abs(self.longitude - longitude).argmin()

        return self.mean_correlation_map[lat_idx, lon_idx]

# Example Usage
if __name__ == "__main__":
    lookup = WindCorrelationLookup()

    # Test with exact match (raises error if no exact match found)
    try:
        print(lookup.get_mean_correlation(-27.25, 126.25, mode="exact"))
    except ValueError as e:
        print(e)

    # Test with approximate match (finds nearest point)
    print(lookup.get_mean_correlation(-27, 126.25, mode="approx"))
