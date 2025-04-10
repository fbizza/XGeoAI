from dash import html, dcc
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import json
import pandas as pd

def enrich_with_distances(gdf: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches a GeoDataFrame by expanding the 'distances' column into separate
    numeric columns (e.g., distance_from_0, distance_from_1, ...), making the
    data more accessible and friendly for Plotly Dash visualizations.

    Parameters:
    - gdf: A GeoDataFrame with a 'distances' column containing dictionaries
           (or JSON-formatted strings) of distances to other clusters.

    Returns:
    - Enriched GeoDataFrame with new columns: distance_from_{cluster_id}
    """

    gdf['distances'] = gdf['distances'].apply(
        lambda x: json.loads(x) if isinstance(x, str) else x
    )
    distances_df = pd.json_normalize(gdf['distances'])
    distances_df.columns = [f'distance_from_{col}' for col in distances_df.columns]
    enriched_gdf = pd.concat([gdf, distances_df], axis=1)

    return enriched_gdf

gdf = gpd.read_file('../../data/processed/clusters_cohesion.geojson')

fig = px.choropleth_map(
    gdf,
    geojson=json.loads(gdf.to_json()),
    locations="cluster_id",
    featureidkey="properties.cluster_id",
    color="cohesion",
    color_continuous_scale="Viridis",
    map_style="carto-positron",
    center={"lat": 23, "lon": 54},
    zoom=4.5,
    opacity=0.7,
    labels={"cohesion": "Cohesion (0 = tightest)"},
    title="Cluster Cohesion Map (Interactive)"
)

fig.update_layout(
            map=dict(
                center=dict(
                    lat=-29,
                    lon=135
                ),
                zoom=2,
                style='dark',
            ),
            paper_bgcolor="#121212",
            margin=dict(l=0, r=0, t=0, b=0),
        )


layout = html.Div([
dbc.Container([
                html.H1("Clusters 'importance'", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])