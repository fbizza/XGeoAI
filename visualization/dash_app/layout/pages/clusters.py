from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *
import geopandas as gpd
import plotly.express as px
import json
import pandas as pd

gdf = gpd.read_file('../../data/processed/clusters_cohesion.geojson')

# Create the Plotly choropleth map using the loaded GeoDataFrame
fig = px.choropleth_map(
    gdf,
    geojson=json.loads(gdf.to_json()),
    locations="cluster_id",
    featureidkey="properties.cluster_id",
    color="cohesion",
    color_continuous_scale="RdBu",
    map_style="carto-positron",
    center={"lat": 23, "lon": 54},
    zoom=4.5,
    opacity=0.7,
    labels={"cohesion": "Cohesion (0 = tightest)"},
    title="Cluster Cohesion Map (Interactive)"
)

fig.update_layout(
            map=dict(
                center=dict(
                    lat=-29,
                    lon=135
                ),
                zoom=2,
                style='dark',
            ),
            paper_bgcolor="#121212",
            margin=dict(l=0, r=0, t=0, b=0),
        )


layout = html.Div([
dbc.Container([
                html.H1("Clusters 'importance'", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])