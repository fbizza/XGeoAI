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
        opacity=0.4,
        showlegend=False
    )
    map_figure.add_trace(layer)
    return map_figure

import time

def add_choroplet(geojson_path, df):
    start_time = time.time()

    # Step 1: Load GeoJSON
    geojson_start = time.time()
    geojson = load_json(geojson_path)
    geojson_time = time.time() - geojson_start
    print(f"GeoJSON load time: {geojson_time:.4f} sec")

    # Step 2: Create choropleth map
    choropleth_start = time.time()
    layer = px.choropleth_map(df, geojson=geojson, locations='lga_id', color='final_value',
                               color_continuous_scale="Bluered",
                               range_color=(0, 100),
                               zoom=3,
                               center={"lat": -29, "lon": 135},
                               opacity=0.6,
                               custom_data=['lga_id', 'min_distance_to_grid_km', 'noise', 'final_value']
                               )
    choropleth_time = time.time() - choropleth_start
    print(f"Choropleth map creation time: {choropleth_time:.4f} sec")

    # Step 3: Update layout
    layout_start = time.time()
    layer.update_layout(coloraxis_showscale=False)
    layout_time = time.time() - layout_start
    print(f"Layout update time: {layout_time:.4f} sec")

    # Step 4: Update traces
    traces_start = time.time()
    layer.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",
            "Centroid min distance to grid: %{customdata[1]}",
            "Noise: %{customdata[2]}",
            "final_value: %{customdata[3]}",
        ]),
        showlegend=False
    )
    traces_time = time.time() - traces_start
    print(f"Traces update time: {traces_time:.4f} sec")

    # Step 5: Update map style
    style_start = time.time()
    layer.update_layout(map_style="dark")
    style_time = time.time() - style_start
    print(f"Map style update time: {style_time:.4f} sec")

    # Total execution time
    total_time = time.time() - start_time
    print(f"Total add_choroplet execution time: {total_time:.4f} sec")

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

def plot_mean_correlation_map(data_filepath):
    """Loads the saved DataFrame and plots the mean wind correlation on a map."""
    try:
        df = pd.read_csv(data_filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {data_filepath}")
        return

    fig = go.Figure(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color=df['Mean Correlation'],
            colorscale='Reds',
            colorbar=dict(title='Mean Correlation'),
            opacity=0.8
        ),
        text=df['Mean Correlation'],
    ))

    fig.update_layout(
        map=dict(
            center=dict(
                lat=-29,
                lon=135
            ),
            zoom=2,
            style='dark'
        ),
        margin=dict(l=0, r=0, t=40, b=0)  # Adjust margins
    )

    return fig

def plot_mean_correlation_distance_map(data_filepath):
    """Loads the saved DataFrame and plots the mean wind correlation on a map."""
    try:
        df = pd.read_csv(data_filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {data_filepath}")
        return

    fig = go.Figure(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color=df['Mean Distance'],
            colorscale='Reds',
            colorbar=dict(title='Mean Distance'),
            opacity=0.8
        ),
        text=df['Mean Distance'],
    ))

    fig.update_layout(
        map=dict(
            center=dict(
                lat=-29,
                lon=135
            ),
            zoom=2,
            style='dark'
        ),
        margin=dict(l=0, r=0, t=40, b=0)  # Adjust margins
    )

    return fig


def plot_vs_operating_map(data_filepath, wind_farms_filepath):
    """Loads the saved mean correlation DataFrame and the operating wind farms DataFrame and plots them on a map."""
    try:
        # Load the original mean correlation distance data
        df = pd.read_csv(data_filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {data_filepath}")
        return

    try:
        # Load the operating wind farms data
        wind_farms_df = pd.read_csv(wind_farms_filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {wind_farms_filepath}")
        return

    # Create the map plot
    fig = go.Figure()

    # Add the mean correlation markers (existing ones, assume they are already handled in your data)
    fig.add_trace(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color=df['Mean Distance'],  # Assuming there's a 'Mean Distance' column
            colorscale='Reds',
            colorbar=dict(title='Mean Distance'),
            opacity=0.8
        ),
        text=df['Mean Distance'],
        name="Mean Distance Locations"
    ))

    # Add operating wind farm markers (purple)
    fig.add_trace(go.Scattermap(
        lat=wind_farms_df['Latitude'],
        lon=wind_farms_df['Longitude'],
        mode='markers',
        marker=dict(
            size=6,
            color='purple',
            opacity=0.8,
        ),
        text=wind_farms_df['Asset'],  # Display asset name on hover
        name='Wind Farms'
    ))

    # Add closest land location markers (green)
    fig.add_trace(go.Scattermap(
        lat=wind_farms_df['Closest ERA5 Land Latitude'],
        lon=wind_farms_df['Closest ERA5 Land Longitude'],
        mode='markers',
        marker=dict(
            size=6,
            color='green',
            opacity=0.8,
        ),
        text=wind_farms_df['Asset'],
        name='Closest Land Locations'
    ))

    # Update map layout
    fig.update_layout(
        map=dict(
            center=dict(
                lat=-29,
                lon=135
            ),
            zoom=2,
            style='dark'
        ),
        title="Mean Distance and Operating Wind Farms with Closest Land Locations",
        margin=dict(l=0, r=0, t=40, b=0),  # Adjust margins
        legend=dict(x=0.01, y=0.99),  # Position the legend
    )

    return fig
