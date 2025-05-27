import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *
from config import get_data_path

df_path = get_data_path('basetables', 'suitability_index_basetable_v5.csv')
pareto_df = pd.read_csv(df_path)

def pareto_tiers_fig(df):

    fig = px.scatter_map(df,
                         lon=df['Longitude'],
                         lat=df['Latitude'],
                         custom_data=['pareto_tier'],
                         center={'lat': -29, 'lon': 135},
                         map_style='dark',
                         opacity=0.7,
                         zoom=3,
                         color=df['pareto_tier'])

    fig.update_traces(
        hovertemplate="<br>".join([
             "<b>%{customdata[0]}</b>",
            "Pareto tier: %{customdata[0]}",
        ]),
        marker={'size': 6,
        },
)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            align="auto",
            font_size=14,
            font_family="Rockwell"
        ),
        paper_bgcolor="#121212",
    )
    return fig

fig = pareto_tiers_fig(pareto_df)


layout = html.Div([
dbc.Container([
                html.H1("Pareto Tiers", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])


