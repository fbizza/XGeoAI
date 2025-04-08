import pandas as pd
import geopandas as gpd
from tqdm import tqdm

def compute_distance_to_lines(
    df: pd.DataFrame,
    lines_path: str,
    lat_col: str = "Latitude",
    lon_col: str = "Longitude",
    destination_path: str = None) -> pd.DataFrame:
    """
    Compute the minimum distance (in kilometers) from each point in the DataFrame
    to a set of line or multiline geometries (e.g. a grid or network).

    Parameters:
        df (pd.DataFrame): Input DataFrame with latitude and longitude columns.
        lines_path (str): File path to line or multiline geometries (shapefile, geojson, etc.).
        lat_col (str): Name of the latitude column in the DataFrame.
        lon_col (str): Name of the longitude column in the DataFrame.
        destination_path (str, optional): Path to save the result CSV. If None, does not save.

    Returns:
        pd.DataFrame: DataFrame with original coordinates and computed distances in km.
    """

    gdf_points = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326"
    )


    gdf_lines = gpd.read_file(lines_path)
    projected_crs = "EPSG:3577"  #  for Australia, adjust for other regions
    gdf_points = gdf_points.to_crs(projected_crs)
    gdf_lines = gdf_lines.to_crs(projected_crs)

    tqdm.pandas(desc="Computing distances")
    gdf_points['min_distance_to_line_km'] = gdf_points.geometry.progress_apply(
        lambda point: round(gdf_lines.distance(point).min() / 1000, 1)
    )

    result_df = gdf_points[[lon_col, lat_col, 'min_distance_to_line_km']]

    if destination_path:
        result_df.to_csv(destination_path, index=False)

    print(result_df.head)

    return result_df

def geojson_to_dash_friendly():
    import shapely
    import numpy as np
    # TODO: just an example, adjust for use case
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
    return  lats, lons, names

if __name__ == "__main__":
    points_path = '../data/basetables/target_mean_correlation.csv'
    lines_path = '../data/raw/Electricity_Transmission_Lines.geojson'
    destination_path = '../data/basetables/distance_from_grid'

    df = pd.read_csv(points_path)
    result = compute_distance_to_lines(
        df,
        lines_path=lines_path,
        lat_col="Latitude",
        lon_col="Longitude",
        destination_path=destination_path
    )
