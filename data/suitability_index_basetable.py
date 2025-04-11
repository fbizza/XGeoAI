import pandas as pd
from typing import List


def load_data(paths: List[str]) -> List[pd.DataFrame]:
    return [pd.read_csv(path) for path in paths]


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


def merge_multiple_datasets(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    merged_df = dfs[0]
    for i, df in enumerate(dfs[1:], start=2):
        merged_df = pd.merge(merged_df, df, on=["Latitude", "Longitude"], how="inner")
        print(f"Merged with dataset {i}, resulting rows: {len(merged_df)}")
    return merged_df


def normalize_column(series: pd.Series, invert: bool = True) -> pd.Series:
    min_val, max_val = series.min(), series.max()
    normalized = (series - min_val) / (max_val - min_val)
    return 1 - normalized if invert else normalized


def process_data(merged_df: pd.DataFrame) -> pd.DataFrame:
    merged_df['normalized_km'] = normalize_column(merged_df['min_distance_to_line_km'], invert=True)

    merged_df['abs_correlation'] = merged_df['Mean Correlation'].abs()
    merged_df['normalized_corr'] = normalize_column(merged_df['Mean Correlation'], invert=True)

    return merged_df


def build_basetable(merged_df: pd.DataFrame) -> pd.DataFrame:
    return merged_df[['Latitude', 'Longitude', 'normalized_km', 'normalized_corr', "avg_capacity_factor", "avg_wind_speed"]]


def save_basetable(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)


def main():
    paths = [
        "basetables/distance_from_grid",
        "basetables/target_mean_correlation.csv",
        "basetables/avg_wind_speed.csv",
        "basetables/avg_capacity_factor.csv",
    ]

    datasets = load_data(paths)
    validate_all_lat_lon_match(datasets)

    merged_df = merge_multiple_datasets(datasets)
    print(f"Final merged dataset length: {len(merged_df)}")

    processed_df = process_data(merged_df)
    basetable = build_basetable(processed_df)

    print(basetable.head())

    save_basetable(basetable, "basetables/suitability_index_basetable2.csv")


if __name__ == "__main__":
    main()
