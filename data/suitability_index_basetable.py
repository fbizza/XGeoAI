import pandas as pd
import geopandas as gpd
from typing import List, Optional


# ---------- Config ----------
class PipelineConfig:
    def __init__(self,
                 file_paths: List[str],
                 geojson_path: Optional[str] = None,
                 filter_land_only: bool = False,
                 output_path: str = "basetables/suitability_index_basetable.csv"):
        self.file_paths = file_paths
        self.geojson_path = geojson_path
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


# ---------- Step 6: Process ----------
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df['normalized_km'] = normalize_column(df['min_distance_to_line_km'], invert=True)

    df['abs_correlation'] = df['Mean Correlation'].abs()
    df['normalized_corr'] = normalize_column(df['Mean Correlation'], invert=True)

    return df


# ---------- Step 7: Build Final Table ----------
def build_basetable(df: pd.DataFrame) -> pd.DataFrame:
    return df[['Latitude', 'Longitude', 'normalized_km', 'normalized_corr',]]


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

    save_basetable(basetable, config.output_path)

    print("Pipeline complete. Output saved to:", config.output_path)



if __name__ == "__main__":
    config = PipelineConfig(
        file_paths=[
            "basetables/distance_from_grid",
            "basetables/target_mean_correlation.csv",
            "basetables/avg_wind_speed.csv",
            "basetables/avg_capacity_factor.csv",
        ],
        geojson_path="raw/australia_land.json",
        filter_land_only=True,
        output_path="basetables/suitability_index_basetable_in_land.csv"
    )

    run_pipeline(config)
