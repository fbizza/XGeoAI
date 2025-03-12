import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm
from src.map import add_wind_farms, add_grid, add_choroplet
import dash
from dash import dcc, html

df = pd.read_csv('../data/processed/wind-farms.csv')

fig = add_wind_farms(df)
#add_grid(fig)
fig = add_choroplet(fig)

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
