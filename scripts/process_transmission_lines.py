import geopandas as gpd


geojson_file = '../data/raw/Electricity_Transmission_Lines.geojson'
gdf = gpd.read_file(geojson_file)


print(gdf.head())

