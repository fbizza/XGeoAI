from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

suitability_index_df = pd.read_csv('../../data/basetables/suitability_index_basetable_percentiles.csv')
column_name ='min_distance_to_line_km'

def create_distribution_figure(
    df,
    column_name,
    x_axis_label=None,
    title=None,
    highlight_value=None,
):
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    from dash import dcc


    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    if not pd.api.types.is_numeric_dtype(df[column_name]):
        raise ValueError(f"Column '{column_name}' must be numeric.")

    data = df[column_name].dropna()
    hist_vals, bin_edges = np.histogram(data, bins=30, density=True)
    max_density = max(hist_vals)

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data,
        histnorm='probability density',
        marker_color='#17a2b8',
        opacity=0.8,
        hoverinfo="skip",
        name='Distribution'
    ))

    if highlight_value is not None:
        highlight_y = max_density * 1.05 if max_density > 0 else 0.1

        fig.add_trace(go.Scatter(
            x=[highlight_value, highlight_value],
            y=[0, highlight_y],
            mode="lines",
            line=dict(color="red", width=2, dash="dot"),
            hoverinfo="skip"
        ))

        fig.add_annotation(
            x=highlight_value,
            y=highlight_y,
            text=f"Clicked location: {highlight_value:.1f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowcolor="red",
            font=dict(color="white", family="Segoe UI", size=9),
            align="center",
        )


    title_text = title or f"Distribution of {column_name}"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(color='#17a2b8')
        ),
        plot_bgcolor="#1e1e2f",
        paper_bgcolor="#1e1e2f",
        font=dict(color="white"),
        margin=dict(l=40, r=20, t=100, b=20),  # More top space for multi-line titles
        xaxis=dict(
            title=x_axis_label or column_name,
            showgrid=False,
            zeroline=False,
            showline=False,
            color="white"
        ),
        yaxis=dict(
            title='Probability Density',
            range=[0, max_density * 1.3],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False,
            color="white"
        ),
        bargap=0.05,
        showlegend=False,
        hovermode=False
    )

    return dcc.Graph(
        figure=fig,
        config={"displayModeBar": False, "staticPlot": True},
        style={"height": "300px", "border": "none"}
    )


def generate_details_panel_content(point):
    # custom data can be changed from the "create_suitability_index_scattermap_figure" function in plotting_functions.py
    customdata = point.get('customdata', [])
    lat = point.get('lat')
    lon = point.get('lon')
    color = point.get('marker.color')

    return html.Div([
        html.P(f"Latitude: {customdata[0]}"),
        html.P(f"Longitude: {customdata[1]}"),
        html.P(f"Suitability index: {customdata[2]:.1f}"),
        html.P(f"Score distance from grid: {customdata[3]}"),
        html.P(f"Score wind correlation: {customdata[4]}"),
        html.P(f"Score wind capacity factor: {customdata[5]}"),
        html.P(f"Score solar radiation: {customdata[6]}"),

        create_distribution_figure(
            df=suitability_index_df,
            column_name='avg_capacity_factor',
            x_axis_label='Capacity Factor',
            title='Average Capacity Factor',
            highlight_value=customdata[8],
        ),
        create_distribution_figure(
            df=suitability_index_df,
            column_name='avg_solar_radiation',
            x_axis_label="Irradiance (W/m²)",
            title='Average Solar Radiation',
            highlight_value=customdata[10],
        ),
        create_distribution_figure(
            df=suitability_index_df,
            column_name='min_distance_to_line_km',
            x_axis_label='Distance from Grid (km)',
            title='Distance from Electrical Grid',
            highlight_value=customdata[7],
        ),
        create_distribution_figure(
            df=suitability_index_df,
            column_name='Mean Correlation',
            x_axis_label='Correlation',
            title='Correlation with Operating<br>Wind Farms',
            highlight_value=customdata[9],
        ),


    ])