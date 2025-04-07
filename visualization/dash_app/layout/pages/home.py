from dash import html, dcc
import plotly.express as px
import pandas as pd

# Create a sample plotly figure
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", template="plotly_dark")

layout = html.Div([
    html.H1("Home Page", className="text-center text-white mb-4"),
    dcc.Graph(
        figure=fig,
        style={"height": "70vh", "width": "100%"},
        config={"responsive": True}
    )
])
