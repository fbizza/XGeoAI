from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import seaborn as sns
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
import rasterio.features
from affine import Affine
import plotly.express as px
import json as json

from data.data_loader import DataLoader

def hierarchical_clustering(lsmdf, lsmc, rlsmcs5Wmnavg, show=False):
    # replicate Gunn's paper figure
    pairwise_distance_matrix = pairwise_distances(rlsmcs5Wmnavg)
    linkage = sch.linkage(squareform(pairwise_distance_matrix.astype('float32')), method='complete')
    num_clusters = 15  # hard code
    cluster_labels = sch.fcluster(linkage, num_clusters, 'maxclust')
    idxmap = np.empty((np.shape(lsmc)[0] * np.shape(lsmc)[1])) * np.nan
    active_region_indices = np.ndarray.flatten(np.argwhere(np.ndarray.flatten(lsmc) == 1))
    idxmap[active_region_indices] = cluster_labels
    idxmap = idxmap.reshape(np.shape(lsmc)[0], np.shape(lsmc)[1])
    if show:
        plt.pcolor(lsmdf.longitude, lsmdf.latitude, idxmap, cmap='tab20',
                   vmin=0.5, vmax=20.5, alpha=1, snap=True, rasterized=True, zorder=-1)
        plt.show()
    return pairwise_distance_matrix, num_clusters, cluster_labels, idxmap

def distance_matrix(pairwise_distance_matrix, num_clusters, cluster_labels, show=False):
    # avg distances between clusters
    clusters = {}
    for i, label in enumerate(cluster_labels):
        clusters.setdefault(label, []).append(i)

    # calculate average pairwise distance between clusters
    cluster_dist = np.zeros((num_clusters, num_clusters))
    for i in range(1, num_clusters + 1):
        for j in range(1, num_clusters + 1):
            pts_i = clusters[i]
            pts_j = clusters[j]
            dists = pairwise_distance_matrix[np.ix_(pts_i, pts_j)]
            cluster_dist[i - 1, j - 1] = np.mean(dists)

    if show:
        plt.figure(figsize=(10, 8))
        sns.heatmap(cluster_dist, cmap='Purples', annot=True)
        plt.title("Average Distance Between Clusters")
        plt.xlabel("Cluster")
        plt.ylabel("Cluster")
        plt.show()

def clusters_hierarchy(pairwise_distance_matrix, num_clusters, cluster_labels, idxmap, plotly_img=True, save_geojson_path=None):
    # colormap based on within cluster avg distances: tighter clusters -> higher in the hierarchy
    intra_cluster_dists = {}
    for label in range(1, num_clusters + 1):
        pts = np.where(cluster_labels == label)[0]
        if len(pts) > 1:
            submatrix = pairwise_distance_matrix[np.ix_(pts, pts)]
            mean_dist = np.mean(submatrix)
        else:
            mean_dist = 0  # optional: or np.nan if you want to exclude single-point clusters
        intra_cluster_dists[label] = mean_dist

    cohesion_map = np.full((lsmc.shape[0] * lsmc.shape[1]), np.nan)
    active_region_indices = np.flatnonzero(lsmc.flatten() == 1)
    for i, ind in enumerate(active_region_indices):
        cluster_label = cluster_labels[i]
        cohesion_map[ind] = intra_cluster_dists[cluster_label]
    cohesion_map = cohesion_map.reshape(lsmc.shape)

    label_positions = {}
    lat_vals = lsmdf.latitude.values
    lon_vals = lsmdf.longitude.values

    for label in range(1, num_clusters + 1):
        mask = (idxmap == label)

        if np.any(mask):
            # Get the row/col indices of the cluster points
            y_idx, x_idx = np.where(mask)

            # Convert to lat/lon using the grid
            cluster_lats = lat_vals[y_idx]
            cluster_lons = lon_vals[x_idx]

            lat_center = np.mean(cluster_lats)
            lon_center = np.mean(cluster_lons)

            label_positions[label] = (lon_center, lat_center)

    plt.figure(figsize=(10, 8))
    plt.pcolor(lsmdf.longitude, lsmdf.latitude, cohesion_map,
               cmap='viridis', shading='auto', rasterized=True)
    plt.colorbar(label='Cluster Cohesion (lower = tighter)')
    plt.title("Cluster Cohesion Map with Labels")

    # overlay cluster numbers
    for label, (lon, lat) in label_positions.items():
        plt.text(lon, lat, str(label), ha='center', va='center',
                 fontsize=9, fontweight='bold', color='white',
                 bbox=dict(facecolor='black', alpha=0.5, boxstyle='round'))

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.show()

    if plotly_img:
        cohesion_grid = np.nan_to_num(cohesion_map, nan=-1)

        res_lat = lat_vals[1] - lat_vals[0]
        res_lon = lon_vals[1] - lon_vals[0]
        transform = Affine.translation(lon_vals[0] - res_lon / 2, lat_vals[0] - res_lat / 2) * Affine.scale(res_lon,
                                                                                                            res_lat)

        # polygonize
        shapes_gen = rasterio.features.shapes(cohesion_grid.astype(np.float32), transform=transform)

        # extract geometries and values
        geoms = []
        values = []

        for geom, val in shapes_gen:
            if val == -1:
                continue  # skip background
            geoms.append(shape(geom))
            values.append(float(val))

        # create GeoDataFrame
        gdf = gpd.GeoDataFrame({'cohesion': values}, geometry=geoms)
        gdf.set_crs(epsg=4326, inplace=True)

        fig = px.choropleth_map(
            gdf,
            geojson=json.loads(gdf.to_json()),
            locations=gdf.index,
            color="cohesion",
            color_continuous_scale="RdBu",
            map_style="carto-positron",
            center={"lat": np.mean(lat_vals), "lon": np.mean(lon_vals)},
            zoom=4.5,
            opacity=0.7,
            labels={"cohesion": "Cohesion (0 = tightest)"},
            title="Cluster Cohesion Map (Interactive)"
        )

        fig.show()

        if save_geojson_path:
            gdf.to_file(f"{save_geojson_path}/clusters_cohesion.geojson", driver='GeoJSON')



if __name__ == "__main__":
    data_path = "../data/raw"
    loader = DataLoader(data_path)
    lsmdf, lsmc, rlsmcs5Wmnavg = loader.load_wind_correlation_data()
    pairwise_distance_matrix, num_clusters, cluster_labels, idxmap = hierarchical_clustering(lsmdf, lsmc,
                                                                                             rlsmcs5Wmnavg, show=True)
    distance_matrix(pairwise_distance_matrix,
                    num_clusters, cluster_labels, show=True)
    clusters_hierarchy(pairwise_distance_matrix, num_clusters,
                       cluster_labels, idxmap, save_files_path="../data/processed")



