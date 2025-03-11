import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm
from src.map import add_wind_farms
import dash
from dash import dcc, html

df = pd.read_csv('../data/processed/wind-farms.csv')
fig = go.Figure()
fig = add_wind_farms(fig, df)

# def handle():
#     geo_df = gpd.read_file('../data/raw/Electricity_Transmission_Lines.geojson')
#
#     lats = []
#     lons = []
#     names = []
#
#     for feature, name in tqdm(zip(geo_df.geometry, geo_df.get("name", ["Transmission Line"])),
#                               total=len(geo_df), desc="Processing transmission lines"):
#
#
#         if isinstance(feature, shapely.geometry.LineString):
#             line_coords = [feature]
#         elif isinstance(feature, shapely.geometry.MultiLineString):
#             line_coords = feature.geoms
#         else:
#             continue
#
#         for line in line_coords:
#             x, y = line.xy
#             lons.extend(x)
#             lats.extend(y)
#             names.extend([name] * len(y))  # TODO: perhaps divided names?
#             lons.append(None)
#             lats.append(None)
#             names.append(None)
#
#
#     lats = np.array(lats)
#     lons = np.array(lons)
#     names = np.array(names)
#     return lats, lons, names
# lats, lons, names = handle()
#
# fig.add_trace(go.Scattermap(
#     mode="lines",
#     lon=lons,
#     lat=lats,
#     line=dict(width=2, color="red"),
#     name="Transmission Lines",
#     hoverinfo="text"
# ))
fig.show()

# TODO: make it interactive using Dash
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     html.H1("Wind Farms Map"),
#     dcc.Graph(figure=fig)
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
