import pandas as pd
from src.map import add_wind_farms, add_grid, add_choroplet, add_centroids_layer
from src.logic import modify_base_df


CENTROIDS_PATH = '../data/processed/australian-LGAs-centroids.csv'
CENTROIDS_DF = pd.read_csv('../data/processed/australian-LGAs-centroids.csv')
WINDFARMS_DF = pd.read_csv('../data/processed/wind-farms.csv')
LGAS = '../data/processed/georef-australia-local-government-area-ids.geojson'
LGA_IDS_VALUES = pd.read_csv('../data/processed/lgas_values.csv')
ELECTRICITY_GRID = '../data/raw/Electricity_Transmission_Lines.geojson'
destination_path = '../data/processed/LGAs-centroids-distance-to-grid.csv'
CENTROIDS_WITH_DISTANCES_DF = pd.read_csv('../data/processed/LGAs-centroids-distance-to-grid.csv')
BASETABLE_DF = pd.read_csv('../data/basetables/LGAs-basetable.csv')

df = modify_base_df(BASETABLE_DF)

fig = add_choroplet(LGAS, df)

fig = add_wind_farms(WINDFARMS_DF, fig)

fig = add_grid(fig)

#fig = add_centroids_layer(CENTROIDS_WITH_DISTANCES_DF, fig)
fig.show()




# TODO: make it interactive using Dash
