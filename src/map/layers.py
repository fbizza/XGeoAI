import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry
from tqdm import tqdm


path_to_csv = '../data/processed/wind-farms.csv'
def add_wind_farms (df):
    df = pd.read_csv(path_to_csv)

    fig = px.scatter_map(df,
                         lon=df['Longitude'],
                         lat=df['Latitude'],
                         custom_data=['Asset', 'Development Status', 'Capacity (MW_ac)'],
                         center={'lat': -29, 'lon': 135},
                         map_style='dark',
                         zoom=3)

    fig.update_traces(
        hovertemplate="<br>".join([
             "<b>%{customdata[0]}</b>",
            "Development Status: %{customdata[1]}",
            "Capacity: %{customdata[2]}MW",
        ]),
        marker={'size': 6, 'color': 'lightseagreen'}
)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            align="auto",
            font_size=14,
            font_family="Rockwell"
        )
    )

    return fig