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
        margin=dict(l=40, r=20, t=100, b=20),
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


def score_style(score, emphasis=False):
    if score >= 85:
        color = "#2ecc71"  # Excellent
    elif score >= 65:
        color = "#27ae60"  # Very Good
    elif score >= 50:
        color = "#f1c40f"  # Good
    elif score >= 30:
        color = "#e67e22"  # Fair
    elif score >= 15:
        color = "#e74c3c"  # Poor
    else:
        color = "#c0392b"  # Very Poor

    style = {
        "backgroundColor": color,
        "color": "white",
        "padding": "4px 12px" if emphasis else "2px 8px",
        "borderRadius": "6px" if emphasis else "4px",
        "fontWeight": "bold",
        "minWidth": "40px",
        "textAlign": "center",
        "fontSize": "1.2em" if emphasis else "0.9em",
        "boxShadow": "0 0 8px rgba(0,0,0,0.4)" if emphasis else "",
        "marginTop": "5px"
    }
    return style

def generate_details_panel_content(point):
    customdata = point.get('customdata', [])
    lat = point.get('lat')
    lon = point.get('lon')

    return html.Div([
        html.H4("Location Details", style={"marginBottom": "10px", "color": "white"}),

        html.Div([
            html.Div(["Latitude: ", html.Span(f"{customdata[0]}", style={"fontWeight": "bold"})]),
            html.Div(["Longitude: ", html.Span(f"{customdata[1]}", style={"fontWeight": "bold"})]),
        ], style={"marginBottom": "15px", "color": "white"}),

        html.Div([
            html.Div("Suitability Index", style={
                "textAlign": "center",
                "fontSize": "1.1em",
                "fontWeight": "600",
                "marginBottom": "4px",
                "color": "white"
            }),
            html.Div(f"{customdata[2]:.1f}", style={
                **score_style(customdata[2], emphasis=True),
                "margin": "0 auto",
                "textAlign": "center",
                "width": "fit-content"
            }),
        ], style={"margin": "20px 0"}),

        html.H5("Suitability Scores", style={"marginBottom": "5px", "color": "white"}),

        html.Div([
            html.Div([
                html.Span("Distance from Grid:", style={"flex": "1"}),
                html.Span(f"{customdata[3]}", style=score_style(customdata[3]))
            ], style={"display": "flex", "marginBottom": "4px"}),

            html.Div([
                html.Span("Wind Correlation:", style={"flex": "1"}),
                html.Span(f"{customdata[4]}", style=score_style(customdata[4]))
            ], style={"display": "flex", "marginBottom": "4px"}),

            html.Div([
                html.Span("Wind Capacity Factor:", style={"flex": "1"}),
                html.Span(f"{customdata[5]}", style=score_style(customdata[5]))
            ], style={"display": "flex", "marginBottom": "4px"}),

            html.Div([
                html.Span("Solar Radiation:", style={"flex": "1"}),
                html.Span(f"{customdata[6]}", style=score_style(customdata[6]))
            ], style={"display": "flex", "marginBottom": "4px"}),
        ], style={"marginBottom": "20px", "color": "white"}),

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