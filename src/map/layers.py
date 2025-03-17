import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm

from src.map.utils import load_json, line_coords

def add_wind_farms (df, base):

    fig = px.scatter_map(df,
                         lon=df['Longitude'],
                         lat=df['Latitude'],
                         custom_data=['Asset', 'Development Status', 'Capacity (MW_ac)'],
                         center={'lat': -29, 'lon': 135},
                         map_style='dark',
                         opacity=0.7,
                         zoom=3)

    fig.update_traces(
        hovertemplate="<br>".join([
             "<b>%{customdata[0]}</b>",
            "Development Status: %{customdata[1]}",
            "Capacity: %{customdata[2]}MW",
        ]),
        marker={'size': 5, 'color': 'lightseagreen'}
)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            align="auto",
            font_size=14,
            font_family="Rockwell"
        )
    )
    base.add_trace(fig.data[0])
    return base

def add_grid(fig):

    lats, lons, _ = line_coords('../data/processed/Electricity_Transmission_Lines_Dash_Friendly.csv')
    layer = go.Scattermap(
        mode="lines",
        lon=lons,
        lat=lats,
        line=dict(width=1, color="red"),
        name="Transmission Lines",
        hoverinfo="text", #todo: add/remove source text
        opacity=0.4
    )
    fig.add_trace(layer)
    return fig

def add_choroplet(geojson_path, df):

    geojson = load_json(geojson_path)

    layer = px.choropleth_map(df, geojson=geojson, locations='lga', color='value',
                            color_continuous_scale="Teal",
                            range_color=(0, 11),
                            zoom=3, center={"lat": -29, "lon": 135},
                            opacity=0.5,
                            labels={'value': 'A certain metric'},
                            custom_data=['lga', 'value']
                            )
    layer.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",
            "A certain metric: %{customdata[1]}",
        ])
    )
    layer.update_layout(map_style="dark")

    #fig = fig.add_trace(layer.data[0])
    return layer

def add_centroids_layer():
    df = pd.read_csv('../data/processed/australian-LGAs-centroids.csv')

    fig = px.scatter_map(df,
                         lon='Longitude',
                         lat='Latitude',
                         #custom_data=['Random Value'],
                         center={'lat': -29, 'lon': 135},
                         map_style='dark',
                         opacity=0.7,
                         zoom=3)
    fig.show()
