import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm

from src.map.utils import load_json, line_coords

def add_wind_farms (df, map_figure):

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
    map_figure.add_trace(fig.data[0])
    return map_figure

def add_grid(map_figure):

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
    map_figure.add_trace(layer)
    return map_figure

def add_choroplet(geojson_path, df):
    print(df.head())

    geojson = load_json(geojson_path)

    layer = px.choropleth_map(df, geojson=geojson, locations='lga', color='value',
                            color_continuous_scale="Teal",
                            range_color=(0, 11),
                            zoom=3,
                            center={"lat": -29, "lon": 135},
                            opacity=0.1,
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

    #fig = fig.add_trace(layer.data[0]) its base layer (workaround)
    return layer

def add_centroids_layer(df, map_figure):
    # quick fix for overseas territories and standardization TODO: think about something better
    largest_values = df["min_distance_to_grid_km"].nlargest(3).values
    non_outlier_mean = df.loc[~df["min_distance_to_grid_km"].isin(largest_values), "min_distance_to_grid_km"].mean()
    df.loc[df["min_distance_to_grid_km"].isin(largest_values), "min_distance_to_grid_km"] = non_outlier_mean

    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    df["min_distance_to_grid_km"] = np.log1p(df["min_distance_to_grid_km"])
    scaler = StandardScaler()
    df["min_distance_to_grid_km"] = scaler.fit_transform(df[["min_distance_to_grid_km"]])

    plt.figure(figsize=(8, 5))
    plt.hist(df["min_distance_to_grid_km"], bins=10, color="blue", edgecolor="black", alpha=0.7)
    plt.xlabel("Normalized Distance")
    plt.ylabel("Frequency")
    plt.title("Distribution of Normalized Distances")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    layer = px.scatter_map(df,
                         lon='Longitude',
                         lat='Latitude',
                         custom_data=['min_distance_to_grid_km'],
                        )
    # layer2 = px.density_map(df, lat='Latitude', lon='Longitude', z='min_distance_to_grid_m', radius=30)
    layer.update_traces(
        hovertemplate="<br>".join([
            "<b>Distance to grid: %{customdata[0]}</b>"
        ]),
        marker={'size': 8, 'opacity': 1, 'colorscale': 'Jet', 'color': df['min_distance_to_grid_km']}
    )
    map_figure.add_trace(layer.data[0])
    # map_figure.add_trace(layer2.data[0])
    return map_figure
