import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm
from src.map import add_wind_farms, add_grid, add_choroplet, add_centroids_layer
import dash
from dash import dcc, html

df = pd.read_csv('../data/processed/wind-farms.csv')
path = '../data/processed/georef-australia-local-government-area-ids.geojson'
lga_df = pd.read_csv('../data/processed/lgas_values.csv')
# fig = add_choroplet(path, lga_df)
#
#
# fig = add_wind_farms(df, fig)
#
# fig = add_grid(fig)
# fig.show()


add_centroids_layer()



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
