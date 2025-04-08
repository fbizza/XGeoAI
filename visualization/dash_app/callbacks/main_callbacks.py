from dash import html, Input, Output
from visualization.dash_app.layout.pages import (
    grid, mean_correlation_distance, mean_correlation, vs_operating_wind_farms, documentation, home
)


def register_callbacks(app):
    @app.callback(
        Output("sidebar", "className"),
        Input("btn-toggle", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_sidebar(n):
        return "sidebar collapsed" if n % 2 == 1 else "sidebar"

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return home.layout
        elif pathname == "/grid":
            return grid.layout
        elif pathname == "/mean_correlation":
            return mean_correlation.layout
        elif pathname == "/mean_correlation_distance":
            return mean_correlation_distance.layout
        elif pathname == "/vs_operating_wind_farms":
            return vs_operating_wind_farms.layout
        elif pathname == "/documentation":
            return documentation.layout
        return html.Div([html.H1("404 - Page not found")])
