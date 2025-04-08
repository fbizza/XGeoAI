import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *

correlation_df = pd.read_csv("../../data/basetables/target_mean_correlation.csv")
windfarms_df = pd.read_csv("../../data/processed/wind-farms-with-ERA5_coordinates.csv")

correlation_fig = create_scattermap_figure(correlation_df, marker_size=7, colorscale='RdBu', uniform_color=False,
                                           cmin=-0.2, cmax=0.7)

correlation_fig.update_layout(
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

windfarms_fig = create_scattermap_figure(windfarms_df, marker_size=5, value_column_name="Asset", uniform_color="#17A2B8")
windfarms_fig.update_traces(name='Wind Farms')  # set the name for the legend

correlation_fig.update_traces(marker_colorbar_title_font_color="white", selector=dict(type='scattermap'))
correlation_fig.update_traces(marker_colorbar_tickfont_color="white", selector=dict(type='scattermap'))
correlation_fig.update_traces(marker_reversescale=True, selector=dict(type='scattermap'))
correlation_fig.update_traces(name='Correlation')  # set the name for the legend

# fig.update_traces(marker_showscale=False, selector=dict(type='scattermap')) # to remove colorscale

fig = add_map_layer(correlation_fig, windfarms_fig)
fig.update_traces(legendgrouptitle_text="Map Layers", selector=dict(type='scattermap')) # set the title of the legend

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

#fig.update_layout(showlegend=False) # to remove legend


layout = html.Div([
dbc.Container([
                html.H1("Correlation with operating wind farms", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])