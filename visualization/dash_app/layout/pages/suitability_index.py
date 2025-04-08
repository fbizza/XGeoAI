from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from visualization.plotting_functions import *

grid_df = pd.read_csv('../../data/processed/Electricity_Transmission_Lines_Dash_Friendly.csv')
locations_df = pd.read_csv('../../data/basetables/distance_from_grid')



grid_fig = create_lines_figure(grid_df, latitude_column_name="lat", longitude_column_name="lon")
locations_fig = create_scattermap_figure(df=locations_df, value_column_name="min_distance_to_line_km",
                                         colorscale="RdBu", opacity=0.5, marker_size=4)

grid_fig.update_layout(
            map=dict(
                center=dict(
                    lat=-29,
                    lon=135
                ),
                zoom=3,
                style='dark',
            ),
            paper_bgcolor="#121212",
            margin=dict(l=0, r=0, t=0, b=0),
        )

locations_fig.update_traces(marker_reversescale=True, selector=dict(type='scattermap'))

fig = add_map_layer(grid_fig, locations_fig)
fig.update_traces(marker_showscale=False, selector=dict(type='scattermap')) # to remove colorscale
fig.update_layout(showlegend=False)

layout = html.Div([
    dbc.Container([
        html.H1("Suitability Index", className='text-center my-4'),

        dbc.Row([
            # Slider 1 block
            dbc.Col([
                html.Div([
                    html.Label("Wind correlation", className="text-center w-100 mb-2"),
                    dcc.Slider(
                        id='slider-1',
                        min=0,
                        max=1,
                        step=0.01,
                        value=0.5,
                        tooltip={"placement": "top"},
                        marks=None
                    ),
                    html.Div(
                        dcc.Input(
                            id='input-1',
                            type='number',
                            min=0,
                            max=1,
                            step=0.01,
                            value=0.5,
                            className='input-box',
                            style={
                                "width": "15%",
                                "textAlign": "center"
                            }
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=5),

            # Slider 2 block
            dbc.Col([
                html.Div([
                    html.Label("Distance from grid", className="text-center w-100 mb-2"),
                    dcc.Slider(
                        id='slider-2',
                        min=0,
                        max=1,
                        value=0.5,
                        tooltip={"placement": "top"},
                        marks=None
                    ),
                    html.Div(
                        dcc.Input(
                            id='input-2',
                            type='number',
                            min=0,
                            max=1,
                            step=0.01,
                            value=0.5,
                            className='input-box',
                            style={
                                "width": "15%",
                                "textAlign": "center"
                            }
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=5),
        ], justify='center', className="mb-4"),

        # Graph section
        dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
    ])
])



