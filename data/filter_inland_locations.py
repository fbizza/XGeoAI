import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from typing import Optional

def filter_points_within_polygon(
    df: pd.DataFrame,
    geojson_path: str,
    lon_col: str = "Longitude",
    lat_col: str = "Latitude",
    output_path: Optional[str] = None
) -> pd.DataFrame:
    """
    Filters a DataFrame to include only rows where the (lon, lat) points fall within a polygon from a GeoJSON.
    Optionally saves the filtered result as a CSV.

    Parameters:
        df (pd.DataFrame): Input DataFrame with latitude and longitude columns.
        geojson_path (str): Path to GeoJSON file representing the land area.
        lon_col (str): Name of the longitude column. Default is 'Longitude'.
        lat_col (str): Name of the latitude column. Default is 'Latitude'.
        output_path (str, optional): If provided, saves the filtered DataFrame to this CSV file.

    Returns:
        pd.DataFrame: Filtered DataFrame with only land points, same structure as input.
    """
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326"
    )

    land = gpd.read_file(geojson_path)
    unified_land = land.union_all()

    gdf_filtered = gdf[gdf.geometry.within(unified_land)]

    df_filtered = gdf_filtered.drop(columns="geometry")

    if output_path:
        df_filtered.to_csv(output_path, index=False)

    return df_filtered

if __name__ == "__main__":
    df = pd.read_csv("basetables/avg_wind_speed.csv")
    df_filtered = filter_points_within_polygon(
        df,
        geojson_path="raw/australia_land.json",
        output_path="basetables/avg_wind_speed_land_only.csv"
    )

    print("Filtered shape:", df_filtered.shape)