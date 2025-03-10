import folium
import pandas as pd
import json
import webbrowser

# TODO: check working directory and adjust accordingly root to data
# import os
# cwd = os.getcwd()
# print(cwd)


df = pd.read_csv('../data/processed/wind-farms.csv')

m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)

# add wind farm markers
for idx, row in df.iterrows():
    popup = folium.Popup(row['Asset'], max_width=300)

    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=4,
        stroke=False,
        fill=True,
        fill_opacity=1,
        fill_color="orange",
        tooltip=row['Asset']
    ).add_to(m)

geojson_file = '../data/raw/Electricity_Transmission_Lines.geojson'
with open(geojson_file, "r") as f:
    geojson_data = json.load(f)

# add the transmission lines to the map
folium.GeoJson(
    geojson_data,
    name="Electricity Transmission Lines",
    style_function=lambda x: {
        # "color": "blue",
        "weight": 2,
        "opacity": 0.8
    }
).add_to(m)

folium.LayerControl().add_to(m)

map_path = 'folium_map.html'
m.save(map_path)
webbrowser.open(map_path)

