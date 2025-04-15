from dash import html, Input, Output, State, callback_context
import geopandas as gpd
from dash.exceptions import PreventUpdate
from visualization.dash_app.layout.pages import (
    home, mean_correlation_distance, mean_correlation,
    vs_operating_wind_farms, grid, suitability_index, gunn_clusters, clusters,
    interactive_clusters, avg_wind_speed, avg_wind_capacity_factor, documentation
)
from visualization.dash_app.layout.pages.suitability_index import create_map_figure
from visualization.dash_app.layout.pages.interactive_clusters import create_interactive_clusters_map_figure, enrich_with_distances


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
        elif pathname == "/gunn_clusters":
            return gunn_clusters.layout
        elif pathname == "/clusters":
            return clusters.layout
        elif pathname == "/interactive_clusters":
            return interactive_clusters.layout
        elif pathname == "/avg_wind_speed":
            return avg_wind_speed.layout
        elif pathname == "/avg_wind_capacity_factor":
            return avg_wind_capacity_factor.layout
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

    @app.callback(
        Output('slider-3', 'value'),
        Output('input-3', 'value'),
        Input('slider-3', 'value'),
        Input('input-3', 'value'),
    )
    def sync_slider_3(slider_val, input_val):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return (slider_val, slider_val) if triggered_id == 'slider-3' else (input_val, input_val)

    # suitability_index callback:
    @app.callback(
        Output('map-figure', 'figure'),
        Input('input-1', 'value'),
        Input('input-2', 'value'),
        Input('input-3', 'value'),
        State('map-figure', 'relayoutData')  # to keep the same zoom of the figure after update
    )
    def update_map(input_1_value, input_2_value, input_3_value, relayout_data):
        zoom = 2.5
        center = {'lat': -29, 'lon': 135}


        if relayout_data:
            zoom = relayout_data.get('map.zoom', zoom)
            center = relayout_data.get('map.center', center)

        weight_km = input_2_value
        weight_corr = input_1_value
        weight_wind_capacity_factor = input_3_value

        return create_map_figure(weight_km,
                                 weight_corr,
                                 weight_wind_capacity_factor,
                                 zoom,
                                 center=center)


    # interactive_clusters_callback:
    from dash import callback_context
    from dash.exceptions import PreventUpdate

    @app.callback(
        Output("interactive-clusters-map", "figure"),
        [Input("interactive-clusters-map", "clickData"),
         Input("update-clusters-btn", "n_clicks")],  # Listen for button clicks
        State("cluster-count-input", "value"),  # State to get the value of the input
        prevent_initial_call=False  # Allow the callback to run on the initial page load
    )
    def update_cluster_map(clickData, n_clicks, cluster_count):
        # Handle the case where we only want updates from the button
        if n_clicks is None and cluster_count is None:  # Initial page load
            raise PreventUpdate

        # Ensure the cluster_count is within a valid range
        if cluster_count is None or not (1 <= cluster_count <= 100):
            raise PreventUpdate

        # Triggered event
        triggered = [t["prop_id"] for t in callback_context.triggered]

        # Define the file path based on the cluster count
        file_path = f"../../data/processed/wind_clusters/{cluster_count}_clusters.geojson"

        try:
            gdf = gpd.read_file(file_path)
            gdf = enrich_with_distances(gdf)
        except FileNotFoundError:
            raise PreventUpdate

        cluster_num = 1  # Default cluster

        # If the map is clicked, change the cluster number
        if clickData and "interactive-clusters-map.clickData" in triggered:
            cluster_id = clickData["points"][0]["location"]
            cluster_num = int(cluster_id)

        return create_interactive_clusters_map_figure(gdf=gdf, cluster_number=cluster_num)



