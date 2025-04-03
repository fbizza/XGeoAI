import numpy as np
import pickle
import pandas as pd
import plotly.graph_objects as go


class WindCorrelationAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.lsmdf, self.lsmc, self.rlsmcs5Wmnavg = self.load_data()
        self.land_indices = np.argwhere(np.ndarray.flatten(self.lsmc) == 1)
        self.land_coords = np.unravel_index(self.land_indices.flatten(), self.lsmc.shape)
        self.latitude = self.lsmdf.latitude.values
        self.longitude = self.lsmdf.longitude.values

    def load_data(self):
        """Load required datasets."""
        with open(f'{self.data_path}/aus_region_mask.pkl', 'rb') as f:
            lsmdf = pickle.load(f)
        with open(f'{self.data_path}/aus_region_mask_lsmc.pkl', 'rb') as f:
            lsmc = pickle.load(f)
        with open(f'{self.data_path}/wind_correlation_matrix.pkl', 'rb') as f:
            rlsmcs5Wmnavg = pickle.load(f)
        return lsmdf, lsmc, rlsmcs5Wmnavg

    def load_custom_locations(self, file_path, lat_col, lon_col):
        """Load a dataset with user-specified latitude and longitude columns."""
        df = pd.read_csv(file_path)
        target_coords = list(zip(df[lat_col], df[lon_col]))
        return target_coords

    def find_closest_land_point(self, target_lat, target_lon):
        """Find the closest land point in the dataset to the requested coordinates."""
        lat_index = np.argmin(np.abs(self.latitude - target_lat))
        lon_index = np.argmin(np.abs(self.longitude - target_lon))

        land_index = np.where((self.land_coords[0] == lat_index) & (self.land_coords[1] == lon_index))[0]

        if len(land_index) == 0:
            print(f"No land found at ({target_lat}, {target_lon}). Try adjusting the coordinates slightly.")
            return None
        else:
            land_index = land_index[0]  # Extract first match
            closest_lat, closest_lon = self.latitude[lat_index], self.longitude[lon_index]
            print(f"Requested Location: Latitude {target_lat}, Longitude {target_lon}")
            print(f"Closest Land Location Found: Latitude {closest_lat}, Longitude {closest_lon}")
            return land_index, closest_lat, closest_lon

    def get_correlation_values(self, target_coords):
        """Get correlation values based on multiple target locations."""
        correlation_values = np.zeros((len(self.land_coords[0]), len(target_coords)))

        for i, (target_lat, target_lon) in enumerate(target_coords):
            land_index, _, _ = self.find_closest_land_point(target_lat, target_lon)
            if land_index is None:
                return None  # If no valid land point was found, return None
            correlation_values[:, i] = self.rlsmcs5Wmnavg[land_index, :]

        # Compute the mean correlation for each location across the target locations
        mean_correlation = np.mean(correlation_values, axis=1)

        return mean_correlation

    def plot_wind_correlation(self, correlation_values):
        """Plot the wind correlation data on a map."""
        df = pd.DataFrame({
            'Latitude': self.latitude[self.land_coords[0]],
            'Longitude': self.longitude[self.land_coords[1]],
            'Mean Correlation': correlation_values
        })

        fig = go.Figure(go.Scattermap(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers',
            marker=dict(
                size=7,
                color=df['Mean Correlation'],
                colorscale='RdBu',
                colorbar=dict(title='Mean Correlation'),
                opacity=0.8
            ),
        ))

        fig.update_layout(
            title='Wind Correlation Across Australia',
            map=dict(
                style="open-street-map",
                center=dict(lat=-25, lon=135),
                zoom=3
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        fig.show()

    def plot_user_locations(self, target_coords):
        """Plot user-provided locations on the map."""
        df = pd.DataFrame(target_coords, columns=['Latitude', 'Longitude'])

        fig = go.Figure(go.Scattergeo(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers',
            marker=dict(
                size=8,
                color='black',
                symbol='x',
                opacity=0.8
            ),
            name="User Locations"
        ))

        fig.update_layout(
            title="User Locations on Map",
            geo=dict(
                scope='world',
                showland=True,
                landcolor="rgb(229, 229, 229)",
                center=dict(lat=-25, lon=135),
                projection_scale=5  # Adjust to zoom into Australia
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )

        fig.show()


# ================================
# Main Execution
# ================================
if __name__ == "__main__":
    # Path to the data
    data_path = '../../data/raw'

    # Initialize the WindCorrelationAnalysis class
    analysis = WindCorrelationAnalysis(data_path)

    # Load locations from user dataset
    file_path = "../../data/processed/wind-farms-with-ERA5_coordinates.csv"
    lat_col = "Closest ERA5 Land Latitude"
    lon_col = "Closest ERA5 Land Longitude"

    target_coords = analysis.load_custom_locations(file_path, lat_col, lon_col)
    #target_coords = [(-37.65, 147), (-33.75, 116.75), (-15, 132)]

    # Compute and plot the correlation values
    correlation_values = analysis.get_correlation_values(target_coords)
    print(len(target_coords))

    if correlation_values is not None:
        analysis.plot_wind_correlation(correlation_values)

    analysis.plot_user_locations(target_coords)

