import geopandas as gpd
import matplotlib
matplotlib.use("TkAgg") #TODO: think about another plotting way to workaround this error
import matplotlib.pyplot as plt

path = '../data/processed/georef-australia-local-government-area-ids.geojson'
df = gpd.read_file(path)


print("Current CRS:", df.crs)


if df.crs is None or df.crs.to_epsg() == 4326:
    df = df.to_crs(epsg=3577)  #TODO: is it the best proj?

df['centroid'] = df.geometry.centroid


df = df.to_crs(epsg=4326)

centroids = gpd.GeoDataFrame(df, geometry=df['centroid'])


fig, ax = plt.subplots(figsize=(10, 10))
df.plot(ax=ax, color='lightgrey', edgecolor='black', alpha=0.5)
centroids.plot(ax=ax, color='red', markersize=5, label="Centroids")

plt.legend()
plt.title("Centroids of Australian LGAs")
plt.show()
