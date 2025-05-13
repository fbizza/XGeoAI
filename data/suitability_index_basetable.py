import pandas as pd
import geopandas as gpd
from typing import List, Optional

from shapely.geometry import Point

def assign_state_column(df: pd.DataFrame, geojson_data: str) -> pd.DataFrame:
    """
    Adds a 'state' column to a DataFrame based on spatial lookup using GeoJSON data.
    Parameters:
        df (pd.DataFrame): Must contain 'Latitude' and 'Longitude' columns.
        geojson_data (str): Path to GeoJSON file.
    Returns:
        pd.DataFrame: DataFrame with an added 'state' column.
    """
    states_gdf = gpd.read_file(geojson_data).to_crs(epsg=4326)

    df = df.copy()
    df['geometry'] = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    points_gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

    joined = gpd.sjoin(points_gdf, states_gdf[['STATE_NAME', 'geometry']], how='left', predicate='within')
    joined = joined.drop_duplicates(subset=df.index.name or joined.index.name)

    result_df = joined.drop(columns=['geometry', 'index_right'])
    result_df = result_df.rename(columns={'STATE_NAME': 'state'})

    return result_df

# ---------- Config ----------
class PipelineConfig:
    def __init__(self,
                 file_paths: List[str],
                 geojson_path: Optional[str] = None,
                 state_geojson_path: Optional[str] = None,
                 filter_land_only: bool = False,
                 output_path: str = "basetables/suitability_index_basetable.csv"):
        self.file_paths = file_paths
        self.geojson_path = geojson_path
        self.state_geojson_path = state_geojson_path
        self.filter_land_only = filter_land_only
        self.output_path = output_path


# ---------- Step 1: Load ----------
def load_data(paths: List[str]) -> List[pd.DataFrame]:
    return [pd.read_csv(path) for path in paths]


# ---------- Step 2: Validation ----------
def validate_all_lat_lon_match(dfs: List[pd.DataFrame]):
    coord_sets = [set(zip(df['Latitude'], df['Longitude'])) for df in dfs]
    base_coords = coord_sets[0]

    for i, coords in enumerate(coord_sets[1:], start=1):
        if coords != base_coords:
            missing_in_i = base_coords - coords
            extra_in_i = coords - base_coords
            raise ValueError(f"Lat/Lon mismatch in dataset {i + 1}:\n"
                             f"  - Missing coords: {len(missing_in_i)}\n"
                             f"  - Unexpected coords: {len(extra_in_i)}")


# ---------- Step 3: Merge ----------
def merge_multiple_datasets(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    merged_df = dfs[0]
    for i, df in enumerate(dfs[1:], start=2):
        merged_df = pd.merge(merged_df, df, on=["Latitude", "Longitude"], how="inner")
        print(f"Merged with dataset {i}, resulting rows: {len(merged_df)}")
    return merged_df


# ---------- Step 4: Optional Land Filter ----------
def filter_points_within_polygon(
    df: pd.DataFrame,
    geojson_path: str,
    lon_col: str = "Longitude",
    lat_col: str = "Latitude"
) -> pd.DataFrame:
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326"
    )

    land = gpd.read_file(geojson_path)
    unified_land = land.union_all()

    gdf_filtered = gdf[gdf.geometry.within(unified_land)]
    return gdf_filtered.drop(columns="geometry")


# ---------- Step 5: Normalize ----------
def normalize_column(series: pd.Series, invert: bool = True) -> pd.Series:
    min_val, max_val = series.min(), series.max()
    normalized = (series - min_val) / (max_val - min_val)
    return 1 - normalized if invert else normalized

def percentile_score(series: pd.Series, invert: bool = True) -> pd.Series:
    """
    Assigns a score from 1 to 100 based on which percentile a value falls into.
    If invert=True, lower values get higher scores (100 = best).
    If invert=False, higher values get higher scores (100 = best).
    """

    # compute 101 quantile breakpoints for 100 bins
    percentiles = series.quantile([i / 100 for i in range(101)]).values
    percentiles = pd.Series(percentiles).drop_duplicates().values  # remove duplicates to avoid cut errors

    # define score labels: 100 (best) to 1 (worst), or 1 to 100 depending on invert
    if invert:
        labels = list(range(100, 0, -1))  # 100 to 1
    else:
        labels = list(range(1, 101))      # 1 to 100

    # assign percentiles
    scored = pd.cut(series, bins=percentiles, labels=labels, include_lowest=True, duplicates="drop")
    return scored.astype(int)

# ---------- Step 6: Process ----------
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # normalization:
    # df['normalized_km'] = normalize_column(df['min_distance_to_line_km'], invert=True)
    #
    # df['normalized_corr'] = normalize_column(df['Mean Correlation'].abs(), invert=True)
    #
    # df['normalized_wind_capacity_factor'] = normalize_column(df['avg_capacity_factor'], invert=False)
    #
    # df['normalized_solar_radiation'] = normalize_column(df['avg_solar_radiation'], invert=True)
    #
    # return df

    # percentiles:
    df['score_km'] = percentile_score(df['min_distance_to_line_km'], invert=True)

    df['score_wind_correlation'] = percentile_score(df['Mean Correlation'].abs(), invert=True)

    df['score_wind_capacity'] = percentile_score(df['avg_capacity_factor'], invert=False)

    df['score_solar_radiation'] = percentile_score(df['avg_solar_radiation'], invert=True)

    return df


# ---------- Step 7: Build Final Table ----------
def build_basetable(df: pd.DataFrame) -> pd.DataFrame:
    return df[['Latitude', 'Longitude',
               #'normalized_km', 'normalized_corr', 'normalized_wind_capacity_factor', 'normalized_solar_radiation',
               'Mean Correlation', 'min_distance_to_line_km','avg_capacity_factor',
               'avg_solar_radiation',
               'score_km', 'score_wind_correlation', 'score_wind_capacity', 'score_solar_radiation',]]


# ---------- Step 8: Save ----------
def save_basetable(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)


# ---------- Pipeline Runner ----------
def run_pipeline(config: PipelineConfig):
    datasets = load_data(config.file_paths)

    validate_all_lat_lon_match(datasets)

    merged_df = merge_multiple_datasets(datasets)

    # optional land filtering
    if config.filter_land_only:
        if not config.geojson_path:
            raise ValueError("GeoJSON path must be provided when land filtering is enabled.")
        print("Filtering out non-land locations...")
        merged_df = filter_points_within_polygon(merged_df, config.geojson_path)
        print(f"Remaining rows after land filter: {len(merged_df)}")

    processed_df = process_data(merged_df)

    basetable = build_basetable(processed_df)

    if config.state_geojson_path:
        print("Assigning state column...")
        basetable = assign_state_column(basetable, config.state_geojson_path)

    save_basetable(basetable, config.output_path)

    print("Pipeline complete. Output saved to:", config.output_path)



if __name__ == "__main__":
    if __name__ == "__main__":
        config = PipelineConfig(
            file_paths=[
                "basetables/distance_from_grid",
                "basetables/target_mean_correlation.csv",
                "basetables/avg_capacity_factor.csv",
                "basetables/avg_solar_radiation.csv",
            ],
            geojson_path="raw/australia_land.json",  # used for land-only filter
            state_geojson_path="processed/australian_states.geojson",  # used to assign state
            filter_land_only=True,
            output_path="basetables/suitability_index_basetable_v2.csv"
        )

        run_pipeline(config)
