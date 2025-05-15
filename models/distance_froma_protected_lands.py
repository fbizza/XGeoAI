import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Example DataFrame (replace this with your actual df)
df = pd.read_csv('../data/basetables/suitability_index_basetable_v2.csv')

# Load national parks GeoJSON
parks = gpd.read_file("../data/raw/national_reserves_and_conservation_lands.geojson")

# Convert the DataFrame to GeoDataFrame
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Project both to a metric CRS (e.g., EPSG:3857)
gdf_proj = gdf.to_crs(epsg=3857)
parks_proj = parks.to_crs(epsg=3857)

# Compute minimum distance to any national park
gdf_proj["min_distance_nature_land"] = gdf_proj.geometry.apply(
    lambda point: parks_proj.distance(point).min() / 1000  # convert to kilometers
)

# Convert back to original CRS if needed
result = gdf_proj.to_crs(epsg=4326)

# Drop geometry if you want the original DataFrame structure + distance
result = result.drop(columns="geometry")

# Print the head
print(result.head())