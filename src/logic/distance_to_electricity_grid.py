import pandas as pd
import geopandas as gpd
from tqdm import tqdm

def compute_distance(points_path, lines_path, destination_path):
    df = pd.read_csv(points_path)

    gdf_points = gpd.GeoDataFrame(df,
                                  geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
                                  crs="EPSG:4326")

    grid_gdf = gpd.read_file(lines_path)

    projected_crs = "EPSG:3577"
    gdf_points = gdf_points.to_crs(projected_crs)
    grid_gdf = grid_gdf.to_crs(projected_crs)

    tqdm.pandas(desc="Computing distances")
    gdf_points['min_distance_to_grid_km'] = gdf_points.geometry.progress_apply(
        lambda point: round(grid_gdf.geometry.distance(point).min() / 1000, 1))

    result_df = gdf_points[['Longitude', 'Latitude', 'min_distance_to_grid_km']]
    # print(result_df.head())
    result_df.to_csv(destination_path)
    return result_df

if __name__ == "__main__":
    pass
