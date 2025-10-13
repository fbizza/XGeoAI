import geopandas as gpd
import plotly.express as px
import numpy as np
import json

# Load the GeoDataFrame from the saved GeoJSON file
geojson_path = '../../../data/processed/cluster_cohesion.geojson'
gdf = gpd.read_file(geojson_path)


# Create the Plotly choropleth map using the loaded GeoDataFrame
fig = px.choropleth_map(
    gdf,
    geojson=json.loads(gdf.to_json()),
    locations=gdf.index,
    color="cohesion",
    color_continuous_scale="Viridis",
    map_style="carto-positron",
    center={"lat": 23, "lon": 54},
    zoom=4.5,
    opacity=0.7,
    labels={"cohesion": "Cohesion (0 = tightest)"},
    title="Cluster Cohesion Map (Interactive)"
)

# Show the figure
fig.show()
