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


CENTROIDS_DF = pd.read_csv('../data/processed/australian-LGAs-centroids.csv')
WINDFARMS_DF = pd.read_csv('../data/processed/wind-farms.csv')
LGAS = '../data/processed/georef-australia-local-government-area-ids.geojson'
LGA_IDS_VALUES = pd.read_csv('../data/processed/lgas_values.csv')

fig = add_choroplet(LGAS, LGA_IDS_VALUES)

fig = add_wind_farms(WINDFARMS_DF, fig)

fig = add_grid(fig)

fig = add_centroids_layer(CENTROIDS_DF, fig)
fig.show()


#add_centroids_layer(CENTROIDS_DF)



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
