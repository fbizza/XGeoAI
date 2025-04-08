from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from visualization.dash_app.layout.sidebar import sidebar
from visualization.dash_app.callbacks.main_callbacks import register_callbacks

app = Dash(__name__,
           external_stylesheets=[dbc.themes.DARKLY],
           suppress_callback_exceptions=True)

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


