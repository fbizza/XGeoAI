import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go




# Pareto ranking with tier 0 as best
def pareto_ranking(data, cols):
    data = data.copy()
    data['rank'] = -1
    current_rank = 0
    remaining = data.index.tolist()

    while remaining:
        current = data.loc[remaining]
        is_dominated = np.zeros(len(current), dtype=bool)

        for i, row in current.iterrows():
            dominates = (current[cols] >= row[cols]).all(axis=1) & (current[cols] > row[cols]).any(axis=1)
            if dominates.any():
                is_dominated[remaining.index(i)] = True

        front = [idx for idx, dom in zip(remaining, is_dominated) if not dom]
        data.loc[front, 'rank'] = current_rank
        current_rank += 1
        remaining = [idx for idx in remaining if idx not in front]

    return data


# Function to plot Pareto 2D with frontier overlay
def pareto_2d(df, x_col, y_col, frontier_rank=0):
    """
    Plot 2D Pareto fronts with continuous coloring and a frontier line.

    Parameters:
    - df: DataFrame with numeric columns to evaluate
    - x_col: name of x-axis column
    - y_col: name of y-axis column
    - frontier_rank: which tier to plot as the frontier line (e.g., 0 or 1)
    """
    ranked_df = pareto_ranking(df, [x_col, y_col])

    # Only show points with rank >= selected frontier
    plot_df = ranked_df[ranked_df['rank'] >= frontier_rank].copy()

    # Plot
    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        color='rank',
        labels={
            x_col: "Distance to Electrical Grid (score)",
            y_col: "Average Wind Capacity Factor (score)",
            'rank': 'Pareto Rank'
        },
        color_continuous_scale='Viridis',
    )

    fig.update_traces(marker=dict(size=6, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(coloraxis_colorbar=dict(title='Pareto Rank'))

    # Overlay frontier line
    frontier_df = ranked_df[ranked_df['rank'] == frontier_rank].copy()
    frontier_df = frontier_df.sort_values([x_col, y_col])

    fig.add_trace(go.Scatter(
        x=frontier_df[x_col],
        y=frontier_df[y_col],
        mode='lines+markers',
        line=dict(color='black', width=3, dash='dash'),
        marker=dict(symbol='diamond', size=4),
    ))

    fig.show()


from plotly.colors import sample_colorscale

def pareto_3d(df, x_col, y_col, z_col, frontier_rank=0):
    ranked_df = pareto_ranking(df, [x_col, y_col, z_col])

    # Normalize rank for color mapping
    max_rank = ranked_df['rank'].max()
    ranked_df['rank_norm'] = ranked_df['rank'] / max_rank

    # Assign color based on normalized rank
    viridis_colors = sample_colorscale('Viridis', ranked_df['rank_norm'].tolist())
    ranked_df['color'] = viridis_colors

    frontier_df = ranked_df[ranked_df['rank'] <= frontier_rank]
    others_df = ranked_df[ranked_df['rank'] > frontier_rank]

    fig = go.Figure()

    # Frontier group trace (colored by rank, visible by default)
    fig.add_trace(go.Scatter3d(
        x=frontier_df[x_col],
        y=frontier_df[y_col],
        z=frontier_df[z_col],
        mode='markers',
        marker=dict(
            size=5,
            color=frontier_df['color'],
            line=dict(width=0.5, color='DarkSlateGrey'),
        ),
        name=f'Pareto Ranks ≤ {frontier_rank}',
        legendgroup='frontier',
        showlegend=True,
        visible=True
    ))

    # Other ranks trace (colored by rank, hidden by default)
    fig.add_trace(go.Scatter3d(
        x=others_df[x_col],
        y=others_df[y_col],
        z=others_df[z_col],
        mode='markers',
        marker=dict(
            size=4,
            color=others_df['color'],
            line=dict(width=0.5, color='DarkSlateGrey'),
        ),
        name=f'Pareto Ranks > {frontier_rank}',
        legendgroup='others',
        showlegend=True,
        visible='legendonly'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title="Distance to Electrical Grid (score)",
            yaxis_title="Wind Capacity Factor (score)",
            zaxis_title="Wind Speed Correlation (score)",
        ),
        legend_title_text='Pareto Rank Groups',
        coloraxis_colorbar=dict(title='Pareto Rank'),
    )

    fig.show()



if __name__ == "__main__":
    from config import get_data_path
    np.random.seed(29)
    data_path = get_data_path('basetables', 'suitability_index_basetable_v5.csv')
    df = pd.read_csv(data_path)
    subset_df = df.sample(n=1000).reset_index(drop=True)
    pareto_2d(subset_df, x_col='score_km', y_col='score_wind_capacity', frontier_rank=2)
    pareto_3d(subset_df, x_col='score_km', y_col='score_wind_capacity', z_col='score_wind_correlation', frontier_rank=1)


