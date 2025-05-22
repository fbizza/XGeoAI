from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *
import plotly.graph_objects as go
from config import get_data_path

suitability_index_df_data_path = get_data_path('basetables', 'suitability_index_basetable_v6.csv')
df = pd.read_csv(suitability_index_df_data_path)
marker_colors = ['#2ecc71' if val == 1 else '#e74c3c' for val in df['is_suitable_model']]

def create_simple_map(selected_point=None, zoom=3,
                      center={'lat': -29, 'lon': 135}, default_point_lat=-20.0, default_point_lon=142.0):


    fig = go.Figure(go.Scattermap(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        opacity=0.6,
        marker=dict(size=6.5, color=marker_colors),
        customdata=df[['Latitude', 'Longitude']].values,
        hoverinfo='text',
        text=[f"Lat: {lat}, Lon: {lon}" for lat, lon in zip(df['Latitude'], df['Longitude'])],
    ))

    if selected_point:
        fig.add_trace(go.Scattermap(
            lat=[selected_point['lat']],
            lon=[selected_point['lon']],
            mode='markers+text',
            text="Selected Point",
            textposition="bottom right",
            textfont=dict(size=11, color="white", family="Open Sans Bold"),
            marker=dict(
                size=7,
                color='white',
                symbol='circle',
                opacity=1,
                showscale=False
            ),
            hoverinfo="none"

        ))

    if default_point_lat and not selected_point:
        fig.add_trace(go.Scattermap(
            lat=[default_point_lat],
            lon=[default_point_lon],
            mode='markers+text',
            text="Selected Point",
            textposition="bottom right",
            textfont=dict(size=11, color="white", family="Open Sans Bold"),
            marker=dict(
                size=7,
                color='white',
                symbol='circle',
                opacity=1,
                showscale=False
            ),
            hoverinfo="none"
        ))


    fig.update_layout(
        map=dict(center=center, zoom=zoom, style='dark'),
        paper_bgcolor="#121212",
        margin=dict(l=40, r=0, t=0, b=0),
    )
    fig.update_layout(showlegend=False)
    return fig

fig = create_simple_map()

layout = html.Div([
    dbc.Container([
        html.H1("Lime Explainer", className='text-center my-4'),
        html.P([
            "This interactive map shows areas classified by an AI model as ",
            html.Span("suitable", style={'color': '#2ecc71', 'fontWeight': 'bold'}),
            " or ",
            html.Span("not suitable", style={'color': '#e74c3c', 'fontWeight': 'bold'}),
            " for wind farm development. Click on a location to see an explanation of the model’s decision, generated using LIME (Local Interpretable Model-agnostic Explanations)."
        ], className='text-center my-2', style={'fontSize': '0.9rem', 'fontWeight': 'bold'}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Latitude", className="text-center w-100 mb-1",
                                       style={"fontWeight": "500", "fontSize": "0.85rem"}),
                            dcc.Input(
                                id='latitude-input-lime',
                                type='text',
                                value=f"{-20.0:.2f}",
                                className='form-control',
                                disabled=True,
                                readOnly=True,
                                style={
                                    "textAlign": "center",
                                    "border": "1px solid #ced4da",
                                    "borderRadius": "0.25rem",
                                    "padding": "0.25rem 0.5rem",
                                    "fontSize": "0.85rem",
                                    "height": "30px",
                                    "backgroundColor": "#e9ecef",
                                    "userSelect": "none"
                                }
                            )
                        ], width=6),

                        dbc.Col([
                            html.Label("Longitude", className="text-center w-100 mb-1",
                                       style={"fontWeight": "500", "fontSize": "0.85rem"}),
                            dcc.Input(
                                id='longitude-input-lime',
                                type='text',
                                value=f"{142.0:.2f}",
                                className='form-control',
                                disabled=True,
                                readOnly=True,
                                style={
                                    "textAlign": "center",
                                    "border": "1px solid #ced4da",
                                    "borderRadius": "0.25rem",
                                    "padding": "0.25rem 0.5rem",
                                    "fontSize": "0.85rem",
                                    "height": "30px",
                                    "backgroundColor": "#e9ecef",
                                    "userSelect": "none"
                                }
                            )
                        ], width=6)
                    ], className='mb-3'),

                    dbc.Button(
                        "Explain Selected Point",
                        id='explain-btn',
                        className='w-100',
                        style={
                            "backgroundColor": "#17a2b8",
                            "color": "white",
                            "fontWeight": "bold",
                            "border": "none"
                        }
                    )
                ])
            ], width=4),
        ], justify='center', className="mb-4"),



        dcc.Graph(id='lime-map-figure', figure=fig, config={"displayModeBar": False, 'scrollZoom': False}, style={'height': '70vh', 'width': '100%'})
    ])
])
