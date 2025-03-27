import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
import xarray as xr
import random
import geopandas as gpd
from shapely.geometry import Point

# Replace with the path to your downloaded .nc file and GeoJSON file for Australia
file_path = 'wind-data.nc'
geojson_file = '../../data/raw/countries-geojson.geojson'

# Open the NetCDF file using xarray
dataset = xr.open_dataset(file_path)

# Access the wind components (u and v components of wind)
u_wind = dataset['u100']
v_wind = dataset['v100']

# Check the dimension name related to time in your dataset
time_dim = 'valid_time'  # This could be 'valid_time', or the name of the time dimension in your dataset

# Access the data for the first time step
u_wind_t0 = u_wind.isel({time_dim: 0}).values  #
v_wind_t0 = v_wind.isel({time_dim: 0}).values

# Get latitude and longitude values from the dataset
lats = dataset['latitude'].values
lons = dataset['longitude'].values

# GeoJSON file for mainland Australia
australia = gpd.read_file(geojson_file)

australia_mainland = australia[australia['ADMIN'] == 'Australia']

australia_mainland = australia_mainland.to_crs(epsg=4326)

# to not crash the map
num_points = 1000
random_indices = random.sample(range(len(lats) * len(lons)), num_points)

# get the corresponding latitude and longitude for the selected points
selected_lats = [lats[i // len(lons)] for i in random_indices]
selected_lons = [lons[i % len(lons)] for i in random_indices]

# GeoDataFrame for the selected points
selected_points = gpd.GeoDataFrame({
    'geometry': [Point(lon, lat) for lon, lat in zip(selected_lons, selected_lats)]
}, crs="EPSG:4326")

# filter the points that lie within mainland Australia (MultiPolygon handling)
selected_points = selected_points[selected_points.geometry.within(australia_mainland.union_all())]

# get the wind data for the filtered points
filtered_u_wind = [u_wind_t0[i // len(lons), i % len(lons)] for i in selected_points.index]
filtered_v_wind = [v_wind_t0[i // len(lons), i % len(lons)] for i in selected_points.index]


data = {
    'lat': [point.y for point in selected_points.geometry],
    'lon': [point.x for point in selected_points.geometry],
    'u_wind': filtered_u_wind,
    'v_wind': filtered_v_wind
}

df = pd.DataFrame(data)

#TODO: avg over 5 years, and use sqrt(u^2+v^2)

app = dash.Dash(__name__)


fig = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     color='u_wind',  # Color by the u_wind component
                     color_continuous_scale='Viridis',  # Choose a color scale
                     hover_name='u_wind',
                     projection="mercator",
                     title="Wind Data - u100 Component")


fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="white",
        showcoastlines=True,
        coastlinecolor="Black",
    ),
)


app.layout = html.Div([
    html.H1("Wind Data Visualization"),
    dcc.Graph(id='wind-map', figure=fig)
])


if __name__ == '__main__':
    app.run(debug=True)