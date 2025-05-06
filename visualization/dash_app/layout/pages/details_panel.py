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
    highlight_value=None
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
        text_y_offset = highlight_y if highlight_y > 0 else 0.6

        fig.add_trace(go.Scatter(
            x=[highlight_value, highlight_value],
            y=[0, highlight_y],
            mode="lines",
            line=dict(color="red", width=2, dash="dot"),
            hoverinfo="skip"
        ))

        fig.add_annotation(
            x=highlight_value + 0.05,
            y=text_y_offset,
            text=f"Clicked location: {highlight_value}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowcolor="red",
            font=dict(color="white", family="Segoe UI", size=9),
            align="center",
            ax=0,
            ay=-20
        )

    fig.update_layout(
        title=title or f"Distribution of {column_name}",
        plot_bgcolor="#1e1e2f",
        paper_bgcolor="#1e1e2f",
        font=dict(color="white"),
        margin=dict(l=40, r=20, t=70, b=20),
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
        title_font=dict(size=18, color='white', family='Segoe UI'),
        hovermode=False
    )

    return dcc.Graph(
        figure=fig,
        config={"displayModeBar": False, "staticPlot": True},
        style={"height": "300px", "border": "none"}
    )




# def create_figure_1():
#
#     #TODO: add proper distributions figures
#     data = np.random.normal(loc=0, scale=1, size=500)
#
#     fig = go.Figure()
#     fig.add_trace(go.Histogram(
#         x=data,
#         marker_color='#17a2b8',
#         opacity=0.8,
#         hoverlabel=dict(bgcolor="#2c2c3c", font_color="white")
#     ))
#
#     fig.update_layout(
#         title="Distribution 1",
#         plot_bgcolor="#1e1e2f",
#         paper_bgcolor="#1e1e2f",
#         font=dict(color="white"),
#         margin=dict(l=20, r=20, t=40, b=20),
#         xaxis=dict(
#             showgrid=False,
#             zeroline=False,
#             showline=False,
#             color="white"
#         ),
#         yaxis=dict(
#             showgrid=False,
#             zeroline=False,
#             showline=False,
#             color="white"
#         ),
#         bargap=0.05,
#         showlegend=False,
#         title_font=dict(size=18, color='white', family='Segoe UI')
#     )
#
#     return dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "300px", "border": "none"})

def create_figure_2():
    data = np.random.normal(loc=0, scale=1, size=500)
    fig = px.histogram(data, nbins=30, title="Distribution 2")
    fig.update_layout(template="plotly_dark")
    return dcc.Graph(figure=fig)

def create_figure_3():
    data = np.random.normal(loc=0, scale=1, size=500)
    fig = px.histogram(data, nbins=30, title="Distribution 3")
    fig.update_layout(template="plotly_dark")
    return dcc.Graph(figure=fig)

def create_figure_4():
    data = np.random.normal(loc=0, scale=1, size=500)
    fig = px.histogram(data, nbins=30, title="Distribution 4")
    fig.update_layout(template="plotly_dark")
    return dcc.Graph(figure=fig)

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
            column_name='min_distance_to_line_km',
            x_axis_label='Distance from grid (KMs)',
            title='Distance from electrical grid',
            highlight_value=customdata[7],
        ),
        create_figure_2(),
        create_figure_3(),
        create_figure_4(),
    ])