from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *

from config import get_data_path

suitability_index_df_data_path = get_data_path('basetables', 'suitability_index_basetable_v5.csv')
suitability_index_df = pd.read_csv(suitability_index_df_data_path)


# score_km,score_wind_correlation,score_wind_capacity,score_solar_radiation
def add_linear_combination_column(df, weight_km, weight_corr, weight_wind_capacity_factor, weight_solar_radiation, weight_distance_nature_land):
    df['suitability_index'] = ((df['score_km'] * weight_km) +
                               (df['score_wind_correlation'] * weight_corr) +
                               (df['score_wind_capacity'] * weight_wind_capacity_factor) +
                               (df['score_solar_radiation'] * weight_solar_radiation) +
                               (df['score_distance_nature_land'] * weight_distance_nature_land))
    return df


def create_map_figure(weight_km, weight_corr, weight_wind_capacity_factor, weight_solar_radiation, weight_distance_natue_land, zoom=2.5,
                      center={'lat': -29, 'lon': 135}, selected_point=None, selected_state=None, suitability_threshold=None, pareto_tier=None):
    df = add_linear_combination_column(suitability_index_df,
                                       weight_km,
                                       weight_corr,
                                       weight_wind_capacity_factor,
                                       weight_solar_radiation,
                                       weight_distance_natue_land,
                                       )
    custom_colorscale = [
        [0.0, "#B71C1C"],  # Very Poor
        [0.2, "#E53935"],  # Poor
        [0.4, "#FB8C00"],  # Fair
        [0.6, "#FBC02D"],  # Good
        [0.8, "#43A047"],  # Very Good
        [1.0, "#00796B"],  # Excellent
    ]

    if selected_state and selected_state != 'all':
        df = df[df['state'] == selected_state]

    if suitability_threshold and suitability_threshold > 0:
        df = df[df['suitability_index'] >= suitability_threshold]

    if pareto_tier != -1:
        df = df[df['pareto_tier'] <= pareto_tier]


    fig = create_suitability_index_scattermap_figure(
        df=df,
        value_column_name="suitability_index",
        colorscale=custom_colorscale,
        opacity=0.3,
        marker_size=7.5,
        selected_point=selected_point,
        cmin=0,
        cmax=100,
    )
    fig.update_layout(
        map=dict(center=center, zoom=zoom, style='dark'),
        paper_bgcolor="#121212",
        margin=dict(l=40, r=0, t=0, b=0),
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

        #-------------------CONSTRAINTS---------------------##
        dbc.Row([
            # Dropdown for selecting Australian states
            dbc.Col([
                html.Div([
                    html.Label("Select Region", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
                    dcc.Dropdown(
                        id='state-dropdown',
                        options=[
                            {'label': 'All Australia', 'value': 'all'},
                            {'label': 'New South Wales', 'value': 'New South Wales'},
                            {'label': 'Victoria', 'value': 'Victoria'},
                            {'label': 'Queensland', 'value': 'Queensland'},
                            {'label': 'South Australia', 'value': 'South Australia'},
                            {'label': 'Western Australia', 'value': 'Western Australia'},
                            {'label': 'Tasmania', 'value': 'Tasmania'}
                        ],
                        value='all',
                        clearable=False,
                        className='dropdown-box',
                        style={
                            "backgroundColor": "white",
                            "color": "#17A2B8",
                            "border": "1px solid #ced4da",
                            "borderRadius": "0.25rem"
                        },
                    )
                ])
            ], width=3),

            # Slider for suitability index threshold
            dbc.Col([
                html.Div([
                    html.Label("Suitability Threshold", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
                    dcc.Slider(
                        id='suitability-threshold-slider',
                        min=0,
                        max=100,
                        step=1,
                        value=0,
                        tooltip={"placement": "top"},
                        marks=None
                    ),
                    html.Div(
                        dcc.Input(
                            id='suitability-threshold-input',
                            type='number',
                            min=0,
                            max=100,
                            step=1,
                            value=0,
                            className='input-box',
                            style={"width": "20%", "textAlign": "center"}
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=3),

            # Slider for Pareto tiers
            dbc.Col([
                html.Div([
                    html.Label("Maximum Pareto Tier", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
                    dcc.Slider(
                        id='pareto-slider',
                        min=-1,
                        max=14,
                        step=1,
                        value=-1,
                        tooltip={"always_visible": True, "transform": "hideValue", "placement": "top"},
                        marks={
                            **{i: {"label": f"{i}", "style": {"fontSize": "10px"}} for i in range(15)},
                            0: {"label": "0", "style": {"color": "green", "fontSize": "10px"}},
                            14: {"label": "14", "style": {"color": "red", "fontSize": "10px"}}
                        }
                    ),

                ])
            ], width=3),



        ], justify='center', className="mb-4"),




        #-------------------VARIABLES---------------------##
        dbc.Row([
            # Slider 1 block (Wind correlation)
            dbc.Col([
                html.Div([
                    html.Label("Correlation with Existing Farms", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
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
                            style={"width": "30%", "textAlign": "center"}
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=2),

            # Slider 2 block (Distance from grid)
            dbc.Col([
                html.Div([
                    html.Label("Distance to Electrical Grid", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
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
                            style={"width": "30%", "textAlign": "center"}
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=2),

            # Slider 3 Wind Capacity Factor
            dbc.Col([
                            html.Div([
                                html.Label("Wind Capacity Factor", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
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
                                        style={"width": "30%", "textAlign": "center"}
                                    ),
                                    className="d-flex justify-content-center mt-2"
                                )
                            ])
                        ], width=2),

            # Slider 4 block (Solar Radiation)
            dbc.Col([
                html.Div([
                    html.Label("Solar Radiation", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
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
                            style={"width": "30%", "textAlign": "center"}
                        ),
                        className="d-flex justify-content-center mt-2"
                    )
                ])
            ], width=2),

            # Slider 5 Distance from nature land
            dbc.Col([
                            html.Div([
                                html.Label("Distance to Nature Land", className="text-center w-100 mb-2", style={"maxHeight": "3em", "minHeight": "3em"}),
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
                                        style={"width": "30%", "textAlign": "center"}
                                    ),
                                    className="d-flex justify-content-center mt-2"
                                )
                            ])
                        ], width=2),

        ], justify='center', className="mb-4"),



        dcc.Graph(id='map-figure', figure=fig, config={"displayModeBar": False}, style={'height': '70vh', 'width': '100%'})
    ])
])
