import folium
import pandas as pd
import json
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc


df = pd.read_csv('../data/processed/wind-farms.csv')

geojson_file = '../data/raw/Electricity_Transmission_Lines.geojson'
with open(geojson_file, "r") as f:
    geojson_data = json.load(f)


def create_map(num_points):
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)

    # add wind farm markers (limited by num_points)
    for _, row in df.iloc[:num_points].iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=4,
            stroke=False,
            fill=True,
            fill_opacity=1,
            fill_color="orange",
            tooltip=row['Asset']
        ).add_to(m)

    # add transmission lines
    folium.GeoJson(
        geojson_data,
        name="Electricity Transmission Lines",
        style_function=lambda x: {"weight": 2, "opacity": 0.8}
    ).add_to(m)

    return m._repr_html_()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Wind Farm & Transmission Line Map"),

    # slider to control number of wind farms displayed
    dcc.Slider(
        id="num-points-slider",
        min=1,
        max=len(df),
        step=1,
        value=min(50, len(df)),
        marks={i: str(i) for i in range(1, len(df), max(1, len(df) // 10))},  # Dynamic marks
    ),

    html.Br(),

    html.Iframe(id="folium-map", srcDoc=create_map(50), width="100%", height="600px")
])


@app.callback(
    Output("folium-map", "srcDoc"),
    Input("num-points-slider", "value")
)
def update_map(num_points):
    return create_map(num_points)


if __name__ == '__main__':
    app.run(debug=True)
