import numpy as np
import pickle
import pandas as pd
import plotly.graph_objects as go

# Load necessary data
with open('../../../../data/raw/aus_region_mask.pkl', 'rb') as f:
    lsmdf = pickle.load(f)
with open('../../../../data/raw/aus_region_mask_lsmc.pkl', 'rb') as f:
    lsmc = pickle.load(f)
with open('../../../../data/raw/wind_correlation_matrix.pkl', 'rb') as f:
    rlsmcs5Wmnavg = pickle.load(f)

# Calculate mean correlations
mean_correlations = np.mean(rlsmcs5Wmnavg, axis=1)
mean_correlation_map = np.empty(np.shape(lsmc)) * np.nan
land_indices = np.argwhere(np.ndarray.flatten(lsmc) == 1)
land_coords = np.unravel_index(land_indices.flatten(), np.shape(lsmc))
mean_correlation_map[land_coords] = mean_correlations

# Prepare data for plotting
longitude = lsmdf.longitude.values
latitude = lsmdf.latitude.values

# Flatten the data for use in scattermapbox
mean_correlations_flat = np.ndarray.flatten(mean_correlation_map)
mean_correlations_land = mean_correlations_flat[land_indices.flatten()]

df = pd.DataFrame({
    'Latitude': latitude[land_coords[0]],
    'Longitude': longitude[land_coords[1]],
    'Mean Correlation': mean_correlations_land
})

# Create and show the map
fig = go.Figure(go.Scattermap(
    lat=df['Latitude'],
    lon=df['Longitude'],
    mode='markers',
    marker=dict(
        size=5,  # Adjust marker size as needed
        color=df['Mean Correlation'],
        colorscale='RdBu',  # Choose your color scale
        colorbar=dict(title='Mean Correlation'),
        opacity=0.8
    ),
    # text=df['Mean Correlation'],  # Optional: Add text labels
))

fig.update_layout(
    title='Mean Wind Correlation Across Australia',
    mapbox=dict(
        style="open-street-map",  # Choose a map style
        center=dict(lat=-25, lon=135),  # Center the map on Australia
        zoom=3  # Adjust zoom level
    ),
    margin=dict(l=0, r=0, t=40, b=0)  # Adjust margins
)

fig.show()