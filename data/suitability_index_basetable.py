import pandas as pd

distance_from_grid_df = pd.read_csv("basetables/distance_from_grid")
wind_correlation_df = pd.read_csv("basetables/target_mean_correlation.csv")
print(len(wind_correlation_df))
print(len(wind_correlation_df))
print(distance_from_grid_df.head(5))
print(wind_correlation_df.head(5))


merged_df = pd.merge(distance_from_grid_df, wind_correlation_df,
                     on=["Latitude", "Longitude"],
                     how="inner")


print(f"Length of merged dataframe: {len(merged_df)}")
print(merged_df.head(5))

# Normalize the km_distance column (inverted so lower values are better)
km_min = merged_df['min_distance_to_line_km'].min()
km_max = merged_df['min_distance_to_line_km'].max()
merged_df['normalized_km'] = 1 - ((merged_df['min_distance_to_line_km'] - km_min) / (km_max - km_min))

# Normalize the absolute value of the correlation column (inverted so lower absolute values are better)
merged_df['abs_correlation'] = merged_df['Mean Correlation'].abs()
corr_min = merged_df['Mean Correlation'].min()
corr_max = merged_df['Mean Correlation'].max()
merged_df['normalized_corr'] = 1 - ((merged_df['Mean Correlation'] - corr_min) / (corr_max - corr_min))

pd.set_option("display.max_columns", None)

basetable = merged_df[['Latitude', 'Longitude', 'normalized_km', 'normalized_corr']]

print(basetable.head(5))

basetable.to_csv('basetables/suitability_index_basetable.csv', index=False)