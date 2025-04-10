from dash import html
import dash_bootstrap_components as dbc

sidebar = html.Div([
    html.Div(id="sidebar-content", children=[
        html.H2("XGeoAI", className="text-white text-center"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Mean Correlation", href="/mean_correlation", active="exact"),
                dbc.NavLink("Mean Correlation Distance", href="/mean_correlation_distance", active="exact"),
                dbc.NavLink("Vs Operating Wind Farms", href="/vs_operating_wind_farms", active="exact"),
                dbc.NavLink("Grid", href="/grid", active="exact"),
                dbc.NavLink("Suitability Index", href="/suitability_index", active="exact"),
                dbc.NavLink("Clusters", href="/clusters", active="exact"),
                dbc.NavLink("Interactive Clusters", href="/interactive_clusters", active="exact"),
                dbc.NavLink("Documentation", href="/documentation", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ])
], id="sidebar", className="sidebar")
