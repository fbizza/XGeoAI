import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc, html

df = pd.read_csv('../data/processed/wind-farms.csv')

fig = go.Figure()

fig.add_trace(go.Scattermap(
    mode="markers",
    lon=df["Longitude"],
    lat=df["Latitude"],
    marker=dict(size=7, color="orangered"),
    text=df["Asset"],
    hoverinfo="text"
))

# fig.add_trace(go.Scattermap(
#     mode = "markers+lines",
#     lon = [-50, -60,40],
#     lat = [30, 10, -20],
#     marker = {'size': 10}))

fig.update_layout(
    autosize=True,
    map=dict(
        center=dict(
            lat=-29,
            lon=135
        ),
        zoom=3
    ),
)


fig.show()


# TODO: make it interactive using Dash
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     html.H1("Wind Farms Map"),
#     dcc.Graph(figure=fig)
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
