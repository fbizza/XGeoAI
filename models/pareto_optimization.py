import numpy as np
import pandas as pd
import plotly.graph_objects as go

def assign_pareto_tiers(df, score_columns):
    """
    Assign Pareto tiers to a DataFrame based on specified score columns.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - score_columns (list of str): Columns to consider for Pareto analysis (higher is better).

    Returns:
    - df (pd.DataFrame): The DataFrame with a new 'pareto_tier' column (0 = best).
    """
    data = df[score_columns].values
    n = data.shape[0]
    pareto_tiers = np.full(n, -1, dtype=int)

    current_tier = 0
    remaining_indices = np.arange(n)

    while len(remaining_indices) > 0:
        current_data = data[remaining_indices]
        is_pareto = np.ones(current_data.shape[0], dtype=bool)

        for i, point in enumerate(current_data):
            if is_pareto[i]:
                is_dominated = np.all(current_data >= point, axis=1) & np.any(current_data > point, axis=1)
                is_pareto[is_dominated] = False

        tier_indices = remaining_indices[is_pareto]
        pareto_tiers[tier_indices] = current_tier

        remaining_indices = remaining_indices[~is_pareto]
        current_tier += 1

    df['pareto_tier'] = pareto_tiers
    return df


score_columns = [
    'score_km',
    'score_wind_correlation',
    'score_wind_capacity',
    'score_solar_radiation',
    'score_distance_nature_land'
]


def plot_pareto_tier_0(df, marker_size=6, color='green', opacity=0.8):
    df_tier0 = df[df['pareto_tier'] == 0]

    fig = go.Figure(go.Scattermap(
        lat=df_tier0['Latitude'],
        lon=df_tier0['Longitude'],
        mode='markers',
        marker=dict(
            size=marker_size,
            color=color,
            opacity=opacity
        ),
        name='Pareto Tier 0'
    ))

    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox_zoom=6,
        mapbox_center=dict(lat=df_tier0['Latitude'].mean(), lon=df_tier0['Longitude'].mean()),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig



df = pd.read_csv('../data/basetables/suitability_index_basetable_v4.csv')
df = assign_pareto_tiers(df, score_columns)
tier_counts = df['pareto_tier'].value_counts().sort_index()
print(df.head(5))
print("Number of points in each Pareto tier:")
for tier, count in tier_counts.items():
    print(f"  Tier {tier}: {count} points")

fig = plot_pareto_tier_0(df)
fig.show()