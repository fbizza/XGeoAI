from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *


suitability_index_df = pd.read_csv('../../data/basetables/suitability_index_basetable_v5.csv')

# score_km,score_wind_correlation,score_wind_capacity,score_solar_radiation
def add_linear_combination_column(df, weight_km, weight_corr, weight_wind_capacity_factor, weight_solar_radiation, weight_distance_nature_land):
    df['suitability_index'] = ((df['score_km'] * weight_km) +
                               (df['score_wind_correlation'] * weight_corr) +
                               (df['score_wind_capacity'] * weight_wind_capacity_factor) +
                               (df['score_solar_radiation'] * weight_solar_radiation) +
                               (df['score_distance_nature_land'] * weight_distance_nature_land))
    return df


def create_map_figure(weight_km, weight_corr, weight_wind_capacity_factor, weight_solar_radiation, weight_distance_natue_land, zoom=2.5, center={'lat': -29, 'lon': 135}, selected_point=None):
    df = add_linear_combination_column(suitability_index_df,
                                       weight_km,
                                       weight_corr,
                                       weight_wind_capacity_factor,
                                       weight_solar_radiation,
                                       weight_distance_natue_land)
    fig = create_suitability_index_scattermap_figure(
        df=df,
        value_column_name="suitability_index",
        colorscale="RdBu",
        opacity=0.5,
        marker_size=7,
        selected_point=selected_point,
    )
    fig.update_layout(
        map=dict(center=center, zoom=zoom, style='dark'),
        paper_bgcolor="#121212",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    fig.update_traces(marker_reversescale=False, selector=dict(type='scattermap'))
    fig.update_traces(marker_colorbar_title_font_color="white", selector=dict(type='scattermap'))
    fig.update_traces(marker_colorbar_tickfont_color="white", selector=dict(type='scattermap'))
    fig.update_layout(showlegend=False)
    return fig


fig = create_map_figure(weight_km=0.15, weight_corr=0.15, weight_wind_capacity_factor=0.6, weight_solar_radiation=0.1, weight_distance_natue_land=0.0)


layout = html.Div([
    dbc.Container([
        html.H1("Suitability Index", className='text-center my-4'),

        dbc.Row([
            # Slider 1 block (Wind correlation)
            dbc.Col([
                html.Div([
                    html.Label("Wind correlation", className="text-center w-100 mb-2"),
                    dcc.Slider(
                        id='slider-1',
                        min=0,
                        max=1,
                        step=0.01,
                        value=0.15,
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
                            value=0.15,
                            className='input-box',
                            style={"width": "15%", "textAlign": "center"}
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=3),

            # Slider 2 block (Distance from grid)
            dbc.Col([
                html.Div([
                    html.Label("Distance from grid", className="text-center w-100 mb-2"),
                    dcc.Slider(
                        id='slider-2',
                        min=0,
                        max=1,
                        value=0.15,
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
                            value=0.15,
                            className='input-box',
                            style={"width": "15%", "textAlign": "center"}
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=3),

            # Slider 3 Wind Capacity Factor
            dbc.Col([
                            html.Div([
                                html.Label("Wind Capacity Factor", className="text-center w-100 mb-2"),
                                dcc.Slider(
                                    id='slider-3',
                                    min=0,
                                    max=1,
                                    value=0.6,
                                    tooltip={"placement": "top"},
                                    marks=None
                                ),
                                html.Div(
                                    dcc.Input(
                                        id='input-3',
                                        type='number',
                                        min=0,
                                        max=1,
                                        step=0.01,
                                        value=0.6,
                                        className='input-box',
                                        style={"width": "15%", "textAlign": "center"}
                                    ),
                                    className="d-flex justify-content-center mt-2"
                                )
                            ])
                        ], width=3),

            # Slider 4 block (Solar Radiation)
            dbc.Col([
                html.Div([
                    html.Label("Solar Radiation", className="text-center w-100 mb-2"),
                    dcc.Slider(
                        id='slider-4',
                        min=0,
                        max=1,
                        value=0.1,
                        tooltip={"placement": "top"},
                        marks=None
                    ),
                    html.Div(
                        dcc.Input(
                            id='input-4',
                            type='number',
                            min=0,
                            max=1,
                            step=0.01,
                            value=0.1,
                            className='input-box',
                            style={"width": "15%", "textAlign": "center"}
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=3),

            # Slider 5 Distance from nature land
            dbc.Col([
                            html.Div([
                                html.Label("Distance Nature Land", className="text-center w-100 mb-2"),
                                dcc.Slider(
                                    id='slider-5',
                                    min=0,
                                    max=1,
                                    value=0.0,
                                    tooltip={"placement": "top"},
                                    marks=None
                                ),
                                html.Div(
                                    dcc.Input(
                                        id='input-5',
                                        type='number',
                                        min=0,
                                        max=1,
                                        step=0.01,
                                        value=0.0,
                                        className='input-box',
                                        style={"width": "15%", "textAlign": "center"}
                                    ),
                                    className="d-flex justify-content-center mt-2"
                                )
                            ])
                        ], width=3),

        ], justify='center', className="mb-4"),

        dcc.Graph(id='map-figure', figure=fig, config={"displayModeBar": False}, style={'height': '70vh', 'width': '100%'})
    ])
])
