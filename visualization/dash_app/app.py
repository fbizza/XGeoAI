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
        html.A(
            dbc.Button(
                html.Img(src="assets/images/github_logo.png", height="25px"),
                id="btn-2",
                color="secondary",
                className="menu-btn"
            ),
            href="https://github.com/fbizza/XGeoAI",
            target="_blank",
            style={"textDecoration": "none"}
        ),
        html.A(
            dbc.Button(
                html.Img(src="assets/images/monash_uni_logo.png", height="25px"),
                id="btn-3",
                color="secondary",
                className="menu-btn"
            ),
            href="https://www.monash.edu/it",
            target="_blank",
            style={"textDecoration": "none"}
        ),
        # dbc.Button("Button 3", id="btn-3", color="secondary", className="menu-btn"),
    ]),
    sidebar,

    html.Div(id="sidepanel", className="sidepanel collapsed", children=[
        html.Button("✕", id="btn-close-panel", className="close-btn", n_clicks=0),
        html.Div(id="sidepanel-content")
    ]),

    html.Div(id="page-content", className="content"),
])

register_callbacks(app)


