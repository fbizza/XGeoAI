import plotly.graph_objects as go
import pandas as pd

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
