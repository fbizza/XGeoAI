import numpy as np
import pickle
import os
import pandas as pd
import plotly.graph_objects as go

class WindCorrelationLookup:
    def __init__(self, data_folder='../../data/raw/'):
        """Loads data and prepares correlation map."""
        self.data_folder = data_folder
        self._load_data()
        self._compute_correlation_map(method="mean")  # Default to mean correlation

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

    def _compute_correlation_map(self, method="mean"):
        """Computes the correlation map for land points using different aggregation methods."""
        if method == "mean":
            correlations = np.mean(self.rlsmcs5Wmnavg, axis=1)
        elif method == "median":
            correlations = np.median(self.rlsmcs5Wmnavg, axis=1)
        elif method == "std":
            correlations = np.std(self.rlsmcs5Wmnavg, axis=1)
        else:
            raise ValueError("Invalid method. Choose from: 'mean', 'median', 'std'.")

        self.mean_correlation_map = np.full(self.lsmc.shape, np.nan)
        land_indices = np.argwhere(self.lsmc.flatten() == 1)
        land_coords = np.unravel_index(land_indices.flatten(), self.lsmc.shape)

        self.mean_correlation_map[land_coords] = correlations

    def _find_nearest_index(self, lat, lon):
        """Finds the nearest index for a given latitude and longitude."""
        lat_idx = np.abs(self.latitude - lat).argmin()
        lon_idx = np.abs(self.longitude - lon).argmin()
        return lat_idx, lon_idx

    def get_mean_correlation(self, latitude, longitude, mode="exact"):
        """Returns the mean correlation for a given latitude and longitude."""
        if mode not in ["exact", "approx"]:
            raise ValueError("Mode must be 'exact' or 'approx'.")

        lat_idx = np.where(self.latitude == latitude)[0]
        lon_idx = np.where(self.longitude == longitude)[0]

        if mode == "exact":
            if len(lat_idx) == 0 or len(lon_idx) == 0:
                raise ValueError(f"No exact match found for ({latitude}, {longitude})")
            lat_idx, lon_idx = lat_idx[0], lon_idx[0]
        else:
            lat_idx, lon_idx = self._find_nearest_index(latitude, longitude)

        return self.mean_correlation_map[lat_idx, lon_idx]

    def get_correlation_between_points(self, lat1, lon1, lat2, lon2, mode="exact"):
        """
        Returns the correlation between two locations using the correlation matrix.

        Parameters:
        - lat1, lon1: Coordinates of the first location.
        - lat2, lon2: Coordinates of the second location.
        - mode: "exact" (strict match) or "approx" (find nearest point).

        Returns:
        - float: Correlation value between the two locations.
        """
        if mode not in ["exact", "approx"]:
            raise ValueError("Mode must be 'exact' or 'approx'.")

        if mode == "exact":
            lat_idx1, lon_idx1 = np.where(self.latitude == lat1)[0], np.where(self.longitude == lon1)[0]
            lat_idx2, lon_idx2 = np.where(self.latitude == lat2)[0], np.where(self.longitude == lon2)[0]

            if len(lat_idx1) == 0 or len(lon_idx1) == 0 or len(lat_idx2) == 0 or len(lon_idx2) == 0:
                raise ValueError(f"No exact match found for one or both locations.")

            lat_idx1, lon_idx1 = lat_idx1[0], lon_idx1[0]
            lat_idx2, lon_idx2 = lat_idx2[0], lon_idx2[0]

        else:  # Approximate mode
            lat_idx1, lon_idx1 = self._find_nearest_index(lat1, lon1)
            lat_idx2, lon_idx2 = self._find_nearest_index(lat2, lon2)

        # Fetch correlation from the correlation matrix
        correlation_value = self.rlsmcs5Wmnavg[lat_idx1, lat_idx2]
        return correlation_value

    def plot_scztter_map(self, df, value_column):
        """Plots a general map using Plotly, given a DataFrame with latitude, longitude, and a value column.

        Parameters:
        - df (pd.DataFrame): DataFrame containing 'Latitude', 'Longitude', and a value column.
        - value_column (str): The name of the column to visualize.
        - title (str): Title of the plot.
        - colorscale (str): Color scale for the plot.
        """

        if not all(col in df.columns for col in ["Latitude", "Longitude", value_column]):
            raise ValueError(f"DataFrame must contain 'Latitude', 'Longitude', and '{value_column}' columns.")

        fig = go.Figure(go.Scattermap(
            lat=df["Latitude"],
            lon=df["Longitude"],
            mode="markers",
            marker=dict(
                size=10,
                color=df[value_column],
                colorscale="Reds",
                colorbar=dict(title=value_column),
                opacity=0.8
            ),
            text=df[value_column]
        ))

        fig.update_layout(
            map=dict(
                style="dark",
                center=dict(lat=df["Latitude"].mean(), lon=df["Longitude"].mean()),
                zoom=2
            ),
        )

        fig.show()


# Example Usage
if __name__ == "__main__":
    lookup = WindCorrelationLookup()

    # Example 1: Exact match (raises error if not found)
    try:
        print("Mean Correlation:", lookup.get_mean_correlation(-27.25, 126.25, mode="exact"))
    except ValueError as e:
        print(e)

    # Example 2: Approximate match (finds nearest point)
    print("Mean Correlation (Approx):", lookup.get_mean_correlation(-27.21, 126.25, mode="approx"))

    # Example 3: Correlation between two locations (exact)
    try:
        print("Correlation Between Points:",
              lookup.get_correlation_between_points(-27.25, 126.25, -30.0, 130.0, mode="exact"))
    except ValueError as e:
        print(e)

    # Example 4: Correlation between two locations (approx)
    print("Correlation Between Points (Approx):",
          lookup.get_correlation_between_points(-27.23, 126.25, -30.0, 130.0, mode="approx"))

    # Prepare DataFrame and plotting the correlation map
    land_indices = np.argwhere(~np.isnan(lookup.mean_correlation_map))
    latitudes = lookup.latitude[land_indices[:, 0]]
    longitudes = lookup.longitude[land_indices[:, 1]]
    values = lookup.mean_correlation_map[land_indices[:, 0], land_indices[:, 1]]

    df = pd.DataFrame({
        "Latitude": latitudes,
        "Longitude": longitudes,
        "Correlation": values
    })

    # Plot the correlation map
    lookup.plot_scatter_map(df, value_column="Correlation")
