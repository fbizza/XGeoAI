from dash import html, Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
from visualization.dash_app.layout.pages import (
    home, mean_correlation_distance, mean_correlation,
    vs_operating_wind_farms, grid, suitability_index, clusters, interactive_clusters, documentation
)
from visualization.dash_app.layout.pages.suitability_index import create_map_figure
from visualization.dash_app.layout.pages.interactive_clusters import create_interactive_clusters_map_figure


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
        elif pathname == "/mean_correlation":
            return mean_correlation.layout
        elif pathname == "/mean_correlation_distance":
            return mean_correlation_distance.layout
        elif pathname == "/vs_operating_wind_farms":
            return vs_operating_wind_farms.layout
        elif pathname == "/grid":
            return grid.layout
        elif pathname == "/suitability_index":
            return suitability_index.layout
        elif pathname == "/clusters":
            return clusters.layout
        elif pathname == "/interactive_clusters":
            return interactive_clusters.layout
        elif pathname == "/documentation":
            return documentation.layout
        return html.Div([html.H1("404 - Page not found")], className='text-center my-4')

    @app.callback(
        Output('slider-1', 'value'),
        Output('input-1', 'value'),
        Input('slider-1', 'value'),
        Input('input-1', 'value'),
    )
    def sync_slider_1(slider_val, input_val):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return (slider_val, slider_val) if triggered_id == 'slider-1' else (input_val, input_val)

    @app.callback(
        Output('slider-2', 'value'),
        Output('input-2', 'value'),
        Input('slider-2', 'value'),
        Input('input-2', 'value'),
    )
    def sync_slider_2(slider_val, input_val):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return (slider_val, slider_val) if triggered_id == 'slider-2' else (input_val, input_val)

    # suitability_index callback:
    @app.callback(
        Output('map-figure', 'figure'),
        Input('input-1', 'value'),
        Input('input-2', 'value'),
        State('map-figure', 'relayoutData')
    )
    def update_map(input_1_value, input_2_value, relayout_data):
        zoom = 3
        center = {'lat': -29, 'lon': 135}


        if relayout_data:
            zoom = relayout_data.get('map.zoom', zoom)
            center = relayout_data.get('map.center', center)

        weight_km = input_2_value
        weight_corr = input_1_value

        return create_map_figure(weight_km, weight_corr, zoom, center)


    # interactive_clusters_callback:
    @app.callback(
        Output("interactive-clusters-map", "figure"),
        Input("interactive-clusters-map", "clickData"),
        prevent_initial_call=True
    )
    def update_cluster_map(clickData):
        if clickData is None or "points" not in clickData:
            raise PreventUpdate

        cluster_id = clickData["points"][0]["location"]
        cluster_num = int(cluster_id)

        return interactive_clusters.create_interactive_clusters_map_figure(
            gdf=interactive_clusters.gdf,
            cluster_number=cluster_num
        )


