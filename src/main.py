import pandas as pd
from src.map import add_wind_farms, add_grid, add_choroplet, add_centroids_layer
from src.logic import modify_base_df
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

# Load Data
BASETABLE_DF = pd.read_csv('../data/basetables/LGAs-basetable.csv')
LGAS = '../data/processed/georef-australia-local-government-area-ids.geojson'
WINDFARMS_DF = pd.read_csv('../data/processed/wind-farms.csv')

def create_figure(w_distance, w_noise):
    df = modify_base_df(BASETABLE_DF, w_distance, w_noise)
    fig = add_choroplet(LGAS, df)
    fig = add_wind_farms(WINDFARMS_DF, fig)
    fig = add_grid(fig)
    fig.update_layout(template='plotly_dark', margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "XGeoAI"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("XGeoAI", className="display-4"),
        html.Hr(),
        html.P("Navigation", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Map", href="/", active="exact"),
                dbc.NavLink("Documentation", href="/documentation", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

initial_w_distance = 1
initial_w_noise = 0
initial_figure = create_figure(initial_w_distance, initial_w_noise)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dbc.Container([
            html.H1("Wind farms: optimal sites selection", className='text-center my-4'),
            dbc.Row([
                dbc.Col([
                    html.Label("Weight Distance (w_distance)"),
                    dcc.Slider(
                        id='w_distance_slider',
                        min=0,
                        max=1,
                        step=0.01,
                        value=initial_w_distance,
                        marks={0: '0', 1: '1'}
                    ),
                    dcc.Input(
                        id='w_distance',
                        type='number',
                        min=0,
                        max=1,
                        step=0.01,
                        value=initial_w_distance,
                        className='form-control'
                    ),
                ], width=6),

                dbc.Col([
                    html.Label("Weight Noise (w_noise)"),
                    dcc.Slider(
                        id='w_noise_slider',
                        min=0,
                        max=1,
                        step=0.01,
                        value=initial_w_noise,
                        marks={0: '0', 1: '1'}
                    ),
                    dcc.Input(
                        id='w_noise',
                        type='number',
                        min=0,
                        max=1,
                        step=0.01,
                        value=initial_w_noise,
                        className='form-control'
                    ),
                ], width=6),
            ], className='mb-3'),

            dbc.Row([
                dbc.Col([
                    dbc.Button("Update", id='update-button', color='primary', className='mt-2')
                ], width=12, className='text-center')
            ], className='mb-4'),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='map-figure', figure=initial_figure,
                              style={'height': '60vh', 'width': '70%', 'margin': 'auto'})
                ], width=12, className='d-flex justify-content-center')
            ])
        ], fluid=True)
    elif pathname == "/documentation":
        return html.P("To do: add documentation or instructions")
    return html.Div([
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"The pathname {pathname} was not recognised..."),
    ], className="p-3 bg-light rounded-3")


@app.callback(
    Output('map-figure', 'figure'),
    [Input('update-button', 'n_clicks')],
    [State('w_distance', 'value'), State('w_noise', 'value')]
)
def update_map(n_clicks, w_distance, w_noise):
    if w_distance is None or w_noise is None:
        return dash.no_update
    return create_figure(w_distance, w_noise)

@app.callback(
    [Output('w_distance', 'value'), Output('w_noise', 'value')],
    [Input('w_distance_slider', 'value'), Input('w_noise_slider', 'value')]
)
def sync_slider_input(w_distance_slider, w_noise_slider):
    return w_distance_slider, w_noise_slider

if __name__ == "__main__":
    app.run(debug=True)
