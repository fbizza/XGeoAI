import numpy as np
import pickle
import pandas as pd
import plotly.graph_objects as go


# ================================
# Data Loading
# ================================
def load_data():
    """Load required datasets."""
    with open('../../data/raw/aus_region_mask.pkl', 'rb') as f:
        lsmdf = pickle.load(f)
    with open('../../data/raw/aus_region_mask_lsmc.pkl', 'rb') as f:
        lsmc = pickle.load(f)
    with open('../../data/raw/wind_correlation_matrix.pkl', 'rb') as f:
        rlsmcs5Wmnavg = pickle.load(f)

    return lsmdf, lsmc, rlsmcs5Wmnavg


# ================================
# Data Processing
# ================================



def find_closest_land_point(latitude, longitude, land_coords, target_lat, target_lon):
    """Find the closest land point in the dataset to the requested coordinates."""
    lat_index = np.argmin(np.abs(latitude - target_lat))
    lon_index = np.argmin(np.abs(longitude - target_lon))

    land_index = np.where((land_coords[0] == lat_index) & (land_coords[1] == lon_index))[0]

    if len(land_index) == 0:
        print(f"No land found at ({target_lat}, {target_lon}). Try adjusting the coordinates slightly.")
        return None, None, None, None
    else:
        land_index = land_index[0]  # Extract first match
        closest_lat, closest_lon = latitude[lat_index], longitude[lon_index]

        print(f"Requested Location: Latitude {target_lat}, Longitude {target_lon}")
        print(f"Closest Land Location Found: Latitude {closest_lat}, Longitude {closest_lon}")

        return land_index, closest_lat, closest_lon, (lat_index, lon_index)


# ================================
# Visualization
# ================================
def plot_wind_correlation(latitude, longitude, land_coords, correlation_values):
    """Plot the wind correlation data on a map."""
    df = pd.DataFrame({
        'Latitude': latitude[land_coords[0]],
        'Longitude': longitude[land_coords[1]],
        'Correlation': correlation_values
    })

    fig = go.Figure(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=7,
            color=df['Correlation'],
            colorscale='RdBu',
            colorbar=dict(title='Correlation'),
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

def get_correlation_values(rlsmcs5Wmnavg, land_coords, latitude, longitude, target_lat=None, target_lon=None):
    """Get correlation values based on the chosen mode."""
    if target_lat is not None and target_lon is not None:
        # Find the closest land point to the target location
        land_index, _, _, _ = find_closest_land_point(latitude, longitude, land_coords, target_lat, target_lon)

        if land_index is None:
            return None  # If no valid land point was found, return None

        # Return correlation values for the selected target location
        print(rlsmcs5Wmnavg[land_index, :])
        print(rlsmcs5Wmnavg[land_index, :].shape)
        print(len(rlsmcs5Wmnavg[land_index, :]))
        return rlsmcs5Wmnavg[land_index, :]
    else:
        # Compute mean correlation across all locations
        return np.mean(rlsmcs5Wmnavg, axis=1)

# ================================
# Main Execution
# ================================
if __name__ == "__main__":
    # Load data
    lsmdf, lsmc, rlsmcs5Wmnavg = load_data()

    # Compute the land coordinates
    land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)
    land_coords = np.unravel_index(land_indices.flatten(), lsmc.shape)

    # Extract lat/lon values
    longitude = lsmdf.longitude.values
    latitude = lsmdf.latitude.values

    # Choose the mode (mean or specific location)
    mode = "mean"  # Change this to "mean" for mean correlation

    if mode == "specific":
        # Set target location coordinates
        target_lat, target_lon = -37.65, 147

        # Get correlation values for the specific location
        correlation_values = get_correlation_values(rlsmcs5Wmnavg, land_coords, latitude, longitude, target_lat, target_lon)

    elif mode == "mean":
        # Get the mean correlation values across all locations
        correlation_values = get_correlation_values(rlsmcs5Wmnavg, land_coords, latitude, longitude)

    if correlation_values is not None:
        # Plot results
        plot_wind_correlation(latitude, longitude, land_coords, correlation_values)