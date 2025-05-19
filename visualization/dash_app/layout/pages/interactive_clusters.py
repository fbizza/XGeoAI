from dash import html, dcc
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import json
import pandas as pd
from config import get_data_path

gdf_path = get_data_path('processed/wind_clusters', '30_clusters.geojson')
gdf = gpd.read_file(gdf_path)



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

def create_interactive_clusters_map_figure(gdf, cluster_number):
    # Create the Plotly choropleth map using the loaded GeoDataFrame
    fig = px.choropleth_map(
        gdf,
        geojson=json.loads(gdf.to_json()),
        locations="cluster_id",
        featureidkey="properties.cluster_id",
        color=f"distance_from_{cluster_number}",
        color_continuous_scale="Greens",
        map_style="carto-positron",
        center={"lat": 23, "lon": 54},
        zoom=4.5,
        opacity=0.7,
        labels={"cohesion": "Cohesion (0 = tightest)"},
        title="Cluster Cohesion Map (Interactive)",
        custom_data = ["cluster_id", f"distance_from_{cluster_number}"],
    )

    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>Cluster number: %{customdata[0]}</b>",
            "Distance from selected cluster: %{customdata[1]:.0f}",
        ]),
        marker_line_width=0.35,
        marker_line_color="black"
    )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="#17a2b8",
            align="auto",
            font_size=14,
            font_family="Rockwell",
            font_color="#1e1e2f",
        )
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

    return fig

gdf = enrich_with_distances(gdf)
fig = create_interactive_clusters_map_figure(gdf=gdf, cluster_number=1)


layout = html.Div([
    dbc.Container([
        # Centered Heading
        html.H1("Interactive Clusters Distances",
                className='text-center my-4',
                style={'color': '#ffffff', 'font-size': '2.5rem', 'font-weight': 'bold'}),

        # Row for the input box and button (both centered)
        dbc.Row([
            dbc.Col([
                html.Label("Enter number of clusters (1–100):",
                           className="text-center text-light mb-2",
                           style={'font-size': '1.1rem'}),
                dcc.Input(
                    id="cluster-count-input",
                    type="number",
                    min=1,
                    max=100,
                    step=1,
                    value=30,
                    style={
                        'width': '60%',  # Smaller input width
                        'padding': '0.8rem',  # Padding for better usability
                        'border-radius': '12px',  # Rounded corners
                        'border': '1px solid #17A2B8',  # Accent border color
                        'background-color': '#f0f0f0',  # Light background color
                        'font-size': '16px',  # Font size for text
                        'font-weight': 'bold',  # Bold text inside the input box
                        'color': '#17A2B8'  # Text color inside the box
                    }
                ),
                dbc.Button("Update Clusters",
                           id="update-clusters-btn",
                           style={
                               'margin-top': '1rem',
                               'width': '60%',  # Button takes 80% width
                               'padding': '1rem',
                               'border-radius': '12px',
                               'font-size': '16px',
                               'font-weight': 'bold',
                               'text-align': 'center',
                               'background-color': '#17a2b8'
                           })
            ], width=4, className="mx-auto")  # Center the column
        ], justify="center", className="mb-4"),

        # Map
        dcc.Graph(figure=fig, id="interactive-clusters-map", style={'height': '70vh', 'width': '100%'})
    ], fluid=True)
])