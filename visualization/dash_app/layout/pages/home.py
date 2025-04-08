from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px


# Create a sample plotly figure
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", template="plotly_dark")

layout = html.Div([
dbc.Container([
                html.H1("Mean Wind Correlation Map", className='text-center my-4'),
                dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'})
            ], fluid=True)
])


