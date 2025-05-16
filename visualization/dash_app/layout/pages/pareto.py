import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *


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
        marker={'size': 5, #'color': 'lightseagreen'
        }
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

pareto_df = pd.read_csv("../../data/basetables/suitability_index_basetable_v5.csv")


# windfarms_fig = create_scattermap_figure(windfarms_df, marker_size=5, value_column_name="Asset", uniform_color="#17A2B8")
# windfarms_fig.update_traces(name='Wind Farms')  # set the name for the legend

# correlation_fig.update_traces(marker_colorbar_title_font_color="white", selector=dict(type='scattermap'))
# correlation_fig.update_traces(marker_colorbar_tickfont_color="white", selector=dict(type='scattermap'))
# correlation_fig.update_traces(marker_reversescale=True, selector=dict(type='scattermap'))
# correlation_fig.update_traces(name='Correlation')  # set the name for the legend

# fig.update_traces(marker_showscale=False, selector=dict(type='scattermap')) # to remove colorscale

fig = pareto_tiers_fig(pareto_df)


layout = html.Div([
dbc.Container([
                html.H1("Pareto Tiers", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])


