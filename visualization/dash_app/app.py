from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from visualization.dash_app.layout.sidebar import sidebar
from visualization.dash_app.layout.pages import (
    mean_correlation, vs_operating_wind_farms, documentation
)
from visualization.dash_app.layout.pages import home, mean_correlation_distance
from visualization.dash_app.callbacks.main_callbacks import register_callbacks

app = Dash(__name__,
           external_stylesheets=[dbc.themes.DARKLY])

app.title = "XGeoAI"
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="toggle-container", children=[
        dbc.Button("☰", id="btn-toggle", color="secondary", className="menu-btn"),
        dbc.Button("Button 1", id="btn-1", color="secondary", className="menu-btn"),
        dbc.Button("Button 2", id="btn-2", color="secondary", className="menu-btn"),
        dbc.Button("Button 3", id="btn-3", color="secondary", className="menu-btn"),
    ]),
    sidebar,
    html.Div(id="page-content", className="content")
])

register_callbacks(app)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/mean_correlation":
        return mean_correlation.layout
    elif pathname == "/mean_correlation_distance":
        return mean_correlation_distance.layout
    elif pathname == "/vs_operating_wind_farms":
        return vs_operating_wind_farms.layout
    elif pathname == "/documentation":
        return documentation.layout
    return html.Div([html.H1("404 - Page not found")])
