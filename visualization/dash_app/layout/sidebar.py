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
                dbc.NavLink("Local Explainers", href="/local_explanations", active="exact"),
                dbc.NavLink("Gunn's Clusters", href="/gunn_clusters", active="exact"),
                dbc.NavLink("Clusters", href="/clusters", active="exact"),
                dbc.NavLink("Interactive Clusters", href="/interactive_clusters", active="exact"),
                dbc.NavLink("Average Wind Speed", href="/avg_wind_speed", active="exact"),
                dbc.NavLink("Average Wind Capacity Factor", href="/avg_wind_capacity_factor", active="exact"),
                dbc.NavLink("Average Solar Radiation", href="/avg_solar_radiation", active="exact"),
                #dbc.NavLink("Backtest", href="/backtest", active="exact"),
                dbc.NavLink("Pareto", href="/pareto", active="exact"),
                dbc.NavLink("Documentation", href="/documentation", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ])
], id="sidebar", className="sidebar")
