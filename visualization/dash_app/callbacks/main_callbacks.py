from dash import html, Input, Output, State, ctx
import geopandas as gpd

from dash.exceptions import PreventUpdate
from visualization.dash_app.layout.pages import (
    home, mean_correlation_distance, mean_correlation,
    vs_operating_wind_farms, grid, suitability_index, gunn_clusters, clusters,
    interactive_clusters, avg_wind_speed, avg_wind_capacity_factor, avg_solar_radiation,
    backtest, pareto, documentation
)
from visualization.dash_app.layout.pages.suitability_index import create_map_figure
from visualization.dash_app.layout.pages.interactive_clusters import create_interactive_clusters_map_figure, enrich_with_distances
from visualization.dash_app.layout.pages.details_panel import generate_details_panel_content
from config import get_data_path

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
        elif pathname == "/avg_solar_radiation":
            return avg_solar_radiation.layout
        elif pathname == "/backtest":
            return backtest.layout
        elif pathname == "/pareto":
            return pareto.layout
        elif pathname == "/documentation":
            return documentation.layout
        return html.Div([html.H1("404 - Page not found")], className='text-center my-4')

    @app.callback(
        Output('slider-1', 'value'),
        Output('input-1', 'value'),
        Output('slider-2', 'value'),
        Output('input-2', 'value'),
        Output('slider-3', 'value'),
        Output('input-3', 'value'),
        Output('slider-4', 'value'),
        Output('input-4', 'value'),
        Output('slider-5', 'value'),
        Output('input-5', 'value'),
        Input('slider-1', 'value'),
        Input('input-1', 'value'),
        Input('slider-2', 'value'),
        Input('input-2', 'value'),
        Input('slider-3', 'value'),
        Input('input-3', 'value'),
        Input('slider-4', 'value'),
        Input('input-4', 'value'),
        Input('slider-5', 'value'),
        Input('input-5', 'value'),
        prevent_initial_call=True
    )
    def sync_and_balance_weights(s1, i1, s2, i2, s3, i3, s4, i4, s5, i5):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        values = {
            'slider-1': s1, 'input-1': i1,
            'slider-2': s2, 'input-2': i2,
            'slider-3': s3, 'input-3': i3,
            'slider-4': s4, 'input-4': i4,
            'slider-5': s5, 'input-5': i5,
        }

        # sync slider and input
        if 'slider' in triggered_id:
            main_value = values[triggered_id]
            corresponding_input = triggered_id.replace('slider', 'input')
            values[corresponding_input] = main_value
        elif 'input' in triggered_id:
            main_value = values[triggered_id]
            corresponding_slider = triggered_id.replace('input', 'slider')
            values[corresponding_slider] = main_value

        changed_index = int(triggered_id.split('-')[1])

        fixed_value = values[f'slider-{changed_index}']

        remaining = 1.0 - fixed_value
        if remaining < 0:
            fixed_value = 1.0
            remaining = 0.0

        other_indices = [i for i in [1, 2, 3, 4, 5] if i != changed_index]
        total_other = sum(values[f'slider-{i}'] for i in other_indices)

        if total_other == 0:
            for i in other_indices:
                values[f'slider-{i}'] = round(remaining / 4, 2)
                values[f'input-{i}'] = round(remaining / 4, 2)
        else:
            for i in other_indices:
                proportion = values[f'slider-{i}'] / total_other
                new_value = proportion * remaining
                values[f'slider-{i}'] = round(new_value, 2)
                values[f'input-{i}'] = round(new_value, 2)

        values[f'slider-{changed_index}'] = round(fixed_value, 2)
        values[f'input-{changed_index}'] = round(fixed_value, 2)

        return (
            values['slider-1'], values['input-1'],
            values['slider-2'], values['input-2'],
            values['slider-3'], values['input-3'],
            values['slider-4'], values['input-4'],
            values['slider-5'], values['input-5'],
        )

    # suitability_index callback:
    from dash import ctx

    @app.callback(
        Output('map-figure', 'figure'),
        Input('input-1', 'value'),
        Input('input-2', 'value'),
        Input('input-3', 'value'),
        Input('input-4', 'value'),
        Input('input-5', 'value'),
        Input('state-dropdown', 'value'),
        Input('suitability-threshold-input', 'value'),
        Input('pareto-slider', 'value'),
        Input('map-figure', 'clickData'),
        Input('btn-close-panel', 'n_clicks'),
        State('sidepanel', 'className'),
        State('map-figure', 'relayoutData'),
        State('map-figure', 'figure')
    )
    def update_map(input_1_value, input_2_value, input_3_value, input_4_value, input_5_value,
                   selected_state, suitability_threshold, pareto_tier,
                   clickData, close_cliks, sidepanel_class, relayout_data, current_figure):

        zoom = 2.5
        center = {'lat': -29, 'lon': 135}

        if relayout_data:
            zoom = relayout_data.get('map.zoom', zoom)
            center = relayout_data.get('map.center', center)

        triggered = ctx.triggered_id
        selected_point = None

        # If the user just clicked a map point
        if triggered == "map-figure" and clickData:
            selected_point = {
                "lat": clickData["points"][0]["lat"],
                "lon": clickData["points"][0]["lon"]
            }

        # If the panel is open and the user is closing it
        elif triggered == "btn-close-panel" and sidepanel_class == "sidepanel show":
            selected_point = None

        # Otherwise retain the previously selected point
        else:
            for trace in current_figure.get("data", []):
                if trace.get("name") == "Selected Point":
                    lat = trace["lat"][0]
                    lon = trace["lon"][0]
                    selected_point = {"lat": lat, "lon": lon}
                    break

        return create_map_figure(
            input_2_value,
            input_1_value,
            input_3_value,
            input_4_value,
            input_5_value,
            zoom,
            center,
            selected_point,
            selected_state,
            suitability_threshold,
            pareto_tier,
        )


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
        from config import get_data_path

        file_path = get_data_path('processed/wind_clusters', f'{cluster_count}_clusters.geojson')

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


    # clicks on the suitability index map, it opens a sidepanel with details of the clicked point
    @app.callback(
        Output('sidepanel', 'className'),
        Output('sidepanel-content', 'children'),
        Input('map-figure', 'clickData'),
        Input('btn-close-panel', 'n_clicks'),
        State('sidepanel', 'className'),
        prevent_initial_call=True
    )
    def toggle_details_panel(clickData, close_clicks, current_class):
        triggered_id = ctx.triggered_id

        if triggered_id == "btn-close-panel":
            return "sidepanel collapsed", ""

        if triggered_id == "map-figure" and clickData:
            content = generate_details_panel_content(clickData['points'][0])
            return "sidepanel show", content

        raise PreventUpdate


    @app.callback(
        Output('suitability-threshold-slider', 'value'),
        Output('suitability-threshold-input', 'value'),
        Input('suitability-threshold-slider', 'value'),
        Input('suitability-threshold-input', 'value'),
    )
    def sync_slider_input(slider_val, input_val):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'suitability-threshold-slider':
            return slider_val, slider_val
        elif triggered_id == 'suitability-threshold-input':
            # Clamp input value within 0–100
            valid_val = max(0, min(100, input_val if input_val is not None else 0))
            return valid_val, valid_val

        raise PreventUpdate

    #TODO: callback to highlight selected point and callback to synch sliders with suitability score








