import json
import pandas as pd
import random


def add_lga_id_to_df(destination_path):

    try:
        with open('../../data/processed/georef-australia-local-government-area-ids.geojson', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("GeoJSON data loaded successfully.")
    except Exception as e:
        print(f"Error loading GeoJSON file: {e}")
        raise

    try:
        df = pd.read_csv('../../data/processed/LGAs-centroids-distance-to-grid.csv')
        print("Distances df loaded successfully.")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        raise

    lga_ids = []

    # iterate through the features in the GeoJSON to match latitudes and longitudes
    for index, row in df.iterrows():
        matched_id = None
        lat, lon = row['Latitude'], row['Longitude']

        matched = False

        for feature in data["features"]:
            geo_point = feature["properties"]["geo_point_2d"]
            feature_lat = geo_point["lat"]
            feature_lon = geo_point["lon"]


            if abs(lat - feature_lat) < 0.0000001 and abs(lon - feature_lon) < 0.0000001:
                matched_id = feature["id"]
                matched = True
                break

        if not matched:
            raise ValueError(f"Error: No match found for row {index} with Latitude = {lat}, Longitude = {lon}.")

        lga_ids.append(matched_id)

    df['lga_id'] = lga_ids

    print("DataFrame after adding LGA_IDs:")
    print(df.head())

    df.to_csv(destination_path, index=False)

if __name__ == "__main__":
    destination_path = '../../data/basetables/LGAs-basetable.csv'
    add_lga_id_to_df(destination_path)

