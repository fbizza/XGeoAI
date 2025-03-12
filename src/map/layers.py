import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm

from src.map.utils import load_json

path_to_csv = '../data/processed/wind-farms.csv'
def add_wind_farms (df):
    df = pd.read_csv(path_to_csv)

    fig = px.scatter_map(df,
                         lon=df['Longitude'],
                         lat=df['Latitude'],
                         custom_data=['Asset', 'Development Status', 'Capacity (MW_ac)'],
                         center={'lat': -29, 'lon': 135},
                         map_style='dark',
                         zoom=3)

    fig.update_traces(
        hovertemplate="<br>".join([
             "<b>%{customdata[0]}</b>",
            "Development Status: %{customdata[1]}",
            "Capacity: %{customdata[2]}MW",
        ]),
        marker={'size': 6, 'color': 'lightseagreen'}
)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            align="auto",
            font_size=14,
            font_family="Rockwell"
        )
    )

    return fig

geo_df = gpd.read_file('../data/raw/Electricity_Transmission_Lines.geojson')

def handle(): #todo: change this function. pre-save values
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
    return lats, lons, names

def add_grid(fig):


    lats, lons, names = handle()

    fig.add_trace(go.Scattermap(
        mode="lines",
        lon=lons,
        lat=lats,
        line=dict(width=1, color="red"),
        name="Transmission Lines",
        hoverinfo="text"
    ))

def add_choroplet(figa):
    path = '../data/processed/georef-australia-local-government-area-ids.geojson'
    geojson = load_json(path)

    df = pd.read_csv('../data/processed/lgas_values.csv')

    layer = px.choropleth_map(df, geojson=geojson, locations='lga', color='value',
                            color_continuous_scale="Viridis",
                            range_color=(0, 10),
                            map_style="carto-positron",
                            zoom=3, center={"lat": -29, "lon": 135},
                            opacity=0.5,
                            labels={'value': 'a certain metric'}
                            )
    lats, lons, names = handle()

    layer.add_trace(go.Scattermap(
        mode="lines",
        lon=lons,
        lat=lats,
        line=dict(width=1, color="red"),
        name="Transmission Lines",
        hoverinfo="text"
    ))

    df = pd.read_csv(path_to_csv)

    fig = px.scatter_map(df,
                         lon=df['Longitude'],
                         lat=df['Latitude'],
                         custom_data=['Asset', 'Development Status', 'Capacity (MW_ac)'],
                         center={'lat': -29, 'lon': 135},
                         map_style='dark',
                         zoom=3)

    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",
            "Development Status: %{customdata[1]}",
            "Capacity: %{customdata[2]}MW",
        ]),
        marker={'size': 6, 'color': 'lightseagreen'}
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            align="auto",
            font_size=14,
            font_family="Rockwell"
        )
    )
    layer.add_trace(fig.data[0])
    layer.show()

