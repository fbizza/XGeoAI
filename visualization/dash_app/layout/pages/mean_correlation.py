from dash import html, dcc
import dash_bootstrap_components as dbc
from visualization.plotting_functions import *

df = pd.read_csv("../../data/basetables/all_locations_mean_correlation.csv")

fig = create_scattermap_figure(df, marker_size=7, colorscale='RdBu', uniform_color=False, cmid=0)

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
fig.update_traces(marker_colorbar_title_font_color="white", selector=dict(type='scattermap'))
fig.update_traces(marker_colorbar_tickfont_color="white", selector=dict(type='scattermap'))
fig.update_traces(marker_reversescale=True, selector=dict(type='scattermap'))
# fig.update_traces(marker_showscale=False, selector=dict(type='scattermap')) # to remove colorscale


layout = html.Div([
dbc.Container([
                html.H1("Mean Wind Correlation Map", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])