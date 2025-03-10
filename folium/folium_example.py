import folium
import pandas as pd
import webbrowser

# TODO: check working directory and adjust accordingly root to data
# import os
# cwd = os.getcwd()
# print(cwd)

df = pd.read_csv('../data/processed/wind-farms.csv')

m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)

for idx, row in df.iterrows():
    popup = folium.Popup(row['Asset'], max_width=300)

    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        stroke=False,
        fill=True,
        fill_opacity=1,
        fill_color="green",
        tooltip=row['Asset']
    ).add_to(m)

map_path = 'map_with_minimal_markers.html'
m.save(map_path)

webbrowser.open(f'{map_path}')
