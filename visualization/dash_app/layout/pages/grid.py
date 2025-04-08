from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from visualization.plotting_functions import *
df = pd.read_csv('../../data/processed/Electricity_Transmission_Lines_Dash_Friendly.csv')
fig = create_lines_figure(df, latitude_column_name="lat", longitude_column_name="lon")
fig.update_layout(
            map=dict(
                center=dict(
                    lat=-29,
                    lon=135
                ),
                zoom=2,
                style='dark',
            ),
            paper_bgcolor="#121212",
            margin=dict(l=0, r=0, t=0, b=0),
        )

layout = html.Div([
dbc.Container([
                html.H1("Electricity Grid", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])


