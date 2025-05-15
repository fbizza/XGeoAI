import pandas as pd
import geopandas as gpd
from tqdm import tqdm


def compute_distance_to_parks(
        df: pd.DataFrame,
        parks_path: str,
        lat_col: str = "Latitude",
        lon_col: str = "Longitude",
        destination_path: str = None,
        crs_projected: str = "EPSG:3577"  # Use EPSG:3577 for Australia, 3857 is global web Mercator
) -> pd.DataFrame:
    """
    Compute the minimum distance (in kilometers) from each point in the DataFrame
    to a set of polygon or multipolygon geometries (e.g. national parks).

    Parameters:
        df (pd.DataFrame): Input DataFrame with latitude and longitude columns.
        parks_path (str): File path to polygon geometries (shapefile, geojson, etc.).
        lat_col (str): Name of the latitude column in the DataFrame.
        lon_col (str): Name of the longitude column in the DataFrame.
        destination_path (str, optional): Path to save the result CSV. If None, does not save.
        crs_projected (str): CRS to use for accurate distance calculations.

    Returns:
        pd.DataFrame: Original DataFrame with an added distance column (km).
    """

    # Create GeoDataFrame for input points
    gdf_points = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326"
    )

    # Read park polygons
    gdf_parks = gpd.read_file(parks_path)

    # Reproject to projected CRS for accurate distance calculation
    gdf_points = gdf_points.to_crs(crs_projected)
    gdf_parks = gdf_parks.to_crs(crs_projected)

    tqdm.pandas(desc="Computing distances to parks")
    gdf_points['min_distance_nature_land_km'] = gdf_points.geometry.progress_apply(
        lambda point: round(gdf_parks.distance(point).min() / 1000, 1)
    )

    result_df = gdf_points.drop(columns=["geometry", "Mean Correlation"])

    if destination_path:
        result_df.to_csv(destination_path, index=False)

    print(result_df.head())

    return result_df


if __name__ == "__main__":
    points_path = "../data/basetables/target_mean_correlation.csv"
    parks_path = "../data/raw/national_reserves_and_conservation_lands.geojson"
    destination_path = "../data/basetables/distance_from_nature_lands.csv"

    df = pd.read_csv(points_path)
    result = compute_distance_to_parks(
        df,
        parks_path=parks_path,
        lat_col="Latitude",
        lon_col="Longitude",
        destination_path=destination_path,
        crs_projected="EPSG:3577"
    )
