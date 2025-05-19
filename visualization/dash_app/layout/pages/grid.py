from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from visualization.plotting_functions import *
from config import get_data_path

gird_df_data_path = get_data_path('processed', 'Electricity_Transmission_Lines_Dash_Friendly.csv')
locations_df_data_path = get_data_path('basetables', 'distance_from_grid')

grid_df = pd.read_csv(gird_df_data_path)
locations_df = pd.read_csv(locations_df_data_path)



grid_fig = create_lines_figure(grid_df, latitude_column_name="lat", longitude_column_name="lon")
locations_fig = create_scattermap_figure(df=locations_df, value_column_name="min_distance_to_line_km",
                                         colorscale="RdBu", opacity=0.5, marker_size=4)

grid_fig.update_layout(
            map=dict(
                center=dict(
                    lat=-29,
                    lon=135
                ),
                zoom=3,
                style='dark',
            ),
            paper_bgcolor="#121212",
            margin=dict(l=0, r=0, t=0, b=0),
        )
grid_fig.update_traces(name='Electrical grid')  # set the name for the legend
locations_fig.update_traces(name='Distance')  # set the name for the legend

locations_fig.update_traces(marker_reversescale=True, selector=dict(type='scattermap'))

fig = add_map_layer(grid_fig, locations_fig)
fig.update_traces(marker_showscale=False, selector=dict(type='scattermap')) # to remove colorscale

#fig.update_layout(showlegend=True)
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01,
    font=dict(
        size=12,
        color="white"
    ),
    bgcolor="#1E1E2F",
    grouptitlefont=dict(
        color="white"
    ),
    itemsizing='constant'
))

layout = html.Div([
dbc.Container([
                html.H1("Electrical grid", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])


