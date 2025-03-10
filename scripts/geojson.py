import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm

df = pd.read_csv('../data/processed/wind-farms.csv')

geo_df = gpd.read_file('../data/raw/Electricity_Transmission_Lines.geojson')

lats = []
lons = []
names = []

for feature, name in tqdm(zip(geo_df.geometry, geo_df.get("name", ["Transmission Line"])),
                          total=len(geo_df), desc="Processing transmission lines"):


    if isinstance(feature, shapely.geometry.LineString):
        line_coords = [feature]
    elif isinstance(feature, shapely.geometry.MultiLineString):
        line_coords = feature.geoms
    else:
        continue

    for line in line_coords:
        x, y = line.xy
        lons.extend(x)
        lats.extend(y)
        names.extend([name] * len(y))  # TODO: perhaps divided names?
        lons.append(None)
        lats.append(None)
        names.append(None)


lats = np.array(lats)
lons = np.array(lons)
names = np.array(names)

fig = go.Figure()


fig.add_trace(go.Scattermap(
    mode="markers",
    lon=df["Longitude"],
    lat=df["Latitude"],
    marker=dict(size=7, color="orangered"),
    text=df["Asset"],
    hoverinfo="text",
    name="Wind Farms"
))


fig.add_trace(go.Scattermap(
    mode="lines",
    lon=lons,
    lat=lats,
    line=dict(width=2, color="red"),
    name="Transmission Lines",
    hoverinfo="text"
))


fig.update_layout(
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    map=dict(
        center={'lon': df["Longitude"].mean(), 'lat': df["Latitude"].mean()},
        style="open-street-map",
        zoom=4
    ),
    title="Wind Farms and Transmission Lines",
    showlegend=True
)

# Show the figure
fig.show()
