from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_figure_1():

    #TODO: add proper distributions figures
    data = np.random.normal(loc=0, scale=1, size=500)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data,
        marker_color='#17a2b8',
        opacity=0.8,
        hoverlabel=dict(bgcolor="#2c2c3c", font_color="white")
    ))

    fig.update_layout(
        title="Distribution 1",
        plot_bgcolor="#1e1e2f",
        paper_bgcolor="#1e1e2f",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            color="white"
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            color="white"
        ),
        bargap=0.05,
        showlegend=False,
        title_font=dict(size=18, color='white', family='Segoe UI')
    )

    return dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "300px", "border": "none"})

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
    customdata = point.get('customdata', [])
    lat = point.get('lat')
    lon = point.get('lon')
    color = point.get('marker.color')

    return html.Div([
        html.P(f"Latitude: {lat}"),
        html.P(f"Longitude: {lon}"),
        html.P(f"Custom Data 0: {customdata[0]}"),
        html.P(f"Custom Data 1: {customdata[1]}"),
        html.P(f"Custom Data 2: {customdata[2]}"),
        html.P(f"Color: {color}"),

        create_figure_1(),
        create_figure_2(),
        create_figure_3(),
        create_figure_4(),
    ])