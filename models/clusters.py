import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import squareform
import scipy.cluster.hierarchy as sch
import rasterio.features
from rasterio.transform import Affine
from shapely.geometry import shape
import geopandas as gpd
import plotly.express as px
import json
import os
from tqdm import tqdm


from data.data_loader import DataLoader


def hierarchical_clustering(lsmdf, lsmc, rlsmcs5Wmnavg, num_clusters=15, show=False):
    """
    Perform hierarchical clustering and return distance matrix, cluster labels and index map.
    """
    distances = pairwise_distances(rlsmcs5Wmnavg)
    linkage_matrix = sch.linkage(squareform(distances.astype('float32')), method='complete')
    labels = sch.fcluster(linkage_matrix, num_clusters, criterion='maxclust')

    idxmap = np.full((lsmc.size), np.nan)
    active_idxs = np.flatnonzero(lsmc.flatten() == 1)
    idxmap[active_idxs] = labels
    idxmap = idxmap.reshape(lsmc.shape)

    if show:
        plt.pcolor(lsmdf.longitude, lsmdf.latitude, idxmap, cmap='tab20', vmin=0.5, vmax=20.5)
        plt.title("Hierarchical Clustering")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

    return distances, num_clusters, labels, idxmap


def compute_cluster_distances(pairwise_distance_matrix, cluster_labels, num_clusters, show=False):
    """
    Compute average pairwise distance between clusters and optionally plot heatmap.
    """
    clusters = {i: np.where(cluster_labels == i)[0] for i in range(1, num_clusters + 1)}
    cluster_distances = np.zeros((num_clusters, num_clusters))

    for i in range(1, num_clusters + 1):
        for j in range(1, num_clusters + 1):
            dists = pairwise_distance_matrix[np.ix_(clusters[i], clusters[j])]
            cluster_distances[i - 1, j - 1] = np.mean(dists)

    if show:
        plt.figure(figsize=(10, 8))
        sns.heatmap(cluster_distances, cmap='Purples', annot=True)
        plt.title("Average Distance Between Clusters")
        plt.xlabel("Cluster")
        plt.ylabel("Cluster")
        plt.show()

    return cluster_distances


def compute_intra_cluster_cohesion(pairwise_distance_matrix, cluster_labels, num_clusters):
    """
    Calculate cohesion (intra-cluster distance) for each cluster.
    """
    cohesion = {}
    for label in range(1, num_clusters + 1):
        pts = np.where(cluster_labels == label)[0]
        cohesion[label] = np.mean(pairwise_distance_matrix[np.ix_(pts, pts)]) if len(pts) > 1 else 0
    return cohesion


def build_cohesion_map(lsmc, cluster_labels, cohesion_dict):
    """
    Generate 2D cohesion map based on cluster label cohesion values.
    """
    flat_map = np.full(lsmc.size, np.nan)
    active_idxs = np.flatnonzero(lsmc.flatten() == 1)
    for i, ind in enumerate(active_idxs):
        label = cluster_labels[i]
        flat_map[ind] = cohesion_dict[label]
    return flat_map.reshape(lsmc.shape)


def compute_label_positions(idxmap, lsmdf, num_clusters):
    """
    Compute geographic center (lat/lon) of each cluster.
    """
    positions = {}
    for label in range(1, num_clusters + 1):
        mask = idxmap == label
        if np.any(mask):
            y_idx, x_idx = np.where(mask)
            lat_center = np.mean(lsmdf.latitude.values[y_idx])
            lon_center = np.mean(lsmdf.longitude.values[x_idx])
            positions[label] = (lon_center, lat_center)
    return positions


def plot_static_cohesion_map(lsmdf, cohesion_map, label_positions):
    """
    Plot the static cohesion map with cluster labels.
    """
    plt.figure(figsize=(10, 8))
    plt.pcolor(lsmdf.longitude, lsmdf.latitude, cohesion_map, cmap='viridis', shading='auto')
    plt.colorbar(label='Cluster Cohesion (lower = tighter)')
    plt.title("Cluster Cohesion Map with Labels")
    for label, (lon, lat) in label_positions.items():
        plt.text(lon, lat, str(label), ha='center', va='center', fontsize=9,
                 fontweight='bold', color='white', bbox=dict(facecolor='black', alpha=0.5, boxstyle='round'))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.show()


def create_geojson_plot(lsmdf, lsmc, cluster_labels, cohesion_dict, cluster_distances, save_path=None):
    """
    Generate interactive Plotly map and optionally export GeoJSON file.
    """
    lat_vals = lsmdf.latitude.values
    lon_vals = lsmdf.longitude.values
    res_lat = lat_vals[1] - lat_vals[0]
    res_lon = lon_vals[1] - lon_vals[0]
    transform = Affine.translation(lon_vals[0] - res_lon / 2, lat_vals[0] - res_lat / 2) * Affine.scale(res_lon, res_lat)

    label_grid = np.full(lsmc.shape, -1)
    active_idxs = np.flatnonzero(lsmc.flatten() == 1)
    for i, idx in enumerate(active_idxs):
        label_grid[np.unravel_index(idx, lsmc.shape)] = cluster_labels[i]

    shapes_gen = rasterio.features.shapes(label_grid.astype(np.int32), transform=transform)
    geoms, cluster_ids, cohesions, inter_dists = [], [], [], []

    for geom, cluster_id_raw in shapes_gen:
        cluster_id = int(cluster_id_raw)
        if cluster_id == -1:
            continue
        geoms.append(shape(geom))
        cluster_ids.append(cluster_id)
        cohesions.append(float(cohesion_dict[cluster_id]))
        dist_dict = {
            str(j + 1): float(cluster_distances[cluster_id - 1, j])
            for j in range(cluster_distances.shape[0]) if j + 1 != cluster_id
        }
        inter_dists.append(dist_dict)

    gdf = gpd.GeoDataFrame({
        'cluster_id': cluster_ids,
        'cohesion': cohesions,
        'distances': inter_dists
    }, geometry=geoms, crs='EPSG:4326').dissolve(by='cluster_id', as_index=False, aggfunc='first')

    fig = px.choropleth_map(
        gdf,
        geojson=json.loads(gdf.to_json()),
        locations=gdf.index,
        color="cohesion",
        color_continuous_scale="RdBu",
        map_style="carto-positron",
        center={"lat": np.mean(lat_vals), "lon": np.mean(lon_vals)},
        zoom=2.5,
        opacity=0.7,
        labels={"cohesion": "Cohesion (0 = tightest)"},
        title="Cluster Cohesion Map (Interactive)"
    )
    fig.show()

    if save_path:
        gdf.to_file(f"{save_path}/clusters_cohesion.geojson", driver='GeoJSON')


# In your run_clustering_pipeline function
def run_clustering_pipeline(data_path, save_geojson_path=None):
    print("Loading wind correlation data...")
    loader = DataLoader(data_path)
    lsmdf, lsmc, rlsmcs5Wmnavg = loader.load_wind_correlation_data()

    print("Performing hierarchical clustering...")
    distances, num_clusters, labels, idxmap = hierarchical_clustering(lsmdf, lsmc, rlsmcs5Wmnavg, show=True)

    print("Computing average distances between clusters...")
    cluster_dists = compute_cluster_distances(distances, labels, num_clusters, show=True)

    print("Calculating intra-cluster cohesion...")
    cohesion = compute_intra_cluster_cohesion(distances, labels, num_clusters)

    print("Building cohesion map...")
    cohesion_map = build_cohesion_map(lsmc, labels, cohesion)

    print("Computing label positions...")
    label_positions = compute_label_positions(idxmap, lsmdf, num_clusters)

    print("Plotting static cohesion map...")
    plot_static_cohesion_map(lsmdf, cohesion_map, label_positions)

    print("Creating interactive GeoJSON map and exporting if specified...")
    create_geojson_plot(lsmdf, lsmc, labels, cohesion, cluster_dists, save_path=save_geojson_path)


def generate_multiple_cluster_geojsons(data_path, cluster_values, output_folder):
    """
    Generate GeoJSON files for multiple cluster values without plotting.

    Args:
        data_path (str): Path to the input data.
        cluster_values (list of int): List of number of clusters to generate.
        output_folder (str): Folder to save GeoJSON files (e.g., '../data/processed/clusters').
    """
    loader = DataLoader(data_path)
    lsmdf, lsmc, rlsmcs5Wmnavg = loader.load_wind_correlation_data()

    for num_clusters in tqdm(cluster_values, desc="Generating cluster GeoJSONs"):
        # Step 1: Hierarchical clustering
        distances = pairwise_distances(rlsmcs5Wmnavg)
        linkage_matrix = sch.linkage(squareform(distances.astype('float32')), method='complete')
        labels = sch.fcluster(linkage_matrix, num_clusters, criterion='maxclust')

        # Step 2: Compute cluster distances
        clusters = {i: np.where(labels == i)[0] for i in range(1, num_clusters + 1)}
        cluster_distances = np.zeros((num_clusters, num_clusters))
        for i in range(1, num_clusters + 1):
            for j in range(1, num_clusters + 1):
                dists = distances[np.ix_(clusters[i], clusters[j])]
                cluster_distances[i - 1, j - 1] = np.mean(dists)

        # Step 3: Compute cohesion
        cohesion = {}
        for label in range(1, num_clusters + 1):
            pts = np.where(labels == label)[0]
            cohesion[label] = np.mean(distances[np.ix_(pts, pts)]) if len(pts) > 1 else 0

        # Step 4: Prepare label grid
        lat_vals = lsmdf.latitude.values
        lon_vals = lsmdf.longitude.values
        res_lat = lat_vals[1] - lat_vals[0]
        res_lon = lon_vals[1] - lon_vals[0]
        transform = Affine.translation(lon_vals[0] - res_lon / 2, lat_vals[0] - res_lat / 2) * Affine.scale(res_lon, res_lat)

        label_grid = np.full(lsmc.shape, -1)
        active_idxs = np.flatnonzero(lsmc.flatten() == 1)
        for i, idx in enumerate(active_idxs):
            label_grid[np.unravel_index(idx, lsmc.shape)] = labels[i]

        shapes_gen = rasterio.features.shapes(label_grid.astype(np.int32), transform=transform)
        geoms, cluster_ids, cohesions, inter_dists = [], [], [], []

        for geom, cluster_id_raw in shapes_gen:
            cluster_id = int(cluster_id_raw)
            if cluster_id == -1:
                continue
            geoms.append(shape(geom))
            cluster_ids.append(cluster_id)
            cohesions.append(float(cohesion[cluster_id]))
            dist_dict = {
                str(j + 1): float(cluster_distances[cluster_id - 1, j])
                for j in range(cluster_distances.shape[0]) if j + 1 != cluster_id
            }
            inter_dists.append(dist_dict)

        gdf = gpd.GeoDataFrame({
            'cluster_id': cluster_ids,
            'cohesion': cohesions,
            'distances': inter_dists
        }, geometry=geoms, crs='EPSG:4326').dissolve(by='cluster_id', as_index=False, aggfunc='first')

        # Step 5: Save GeoJSON
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, f"{num_clusters}_clusters.geojson")
        gdf.to_file(file_path, driver='GeoJSON')



if __name__ == "__main__":
    ## for only 1 file and plots use:
    #run_clustering_pipeline(data_path="../data/raw", save_geojson_path="../data/processed")



    cluster_values = [30, 50]
    # cluster_values = list(range(1, 101))


    generate_multiple_cluster_geojsons(
        data_path="../data/raw",
        cluster_values=cluster_values,
        output_folder="../data/processed/wind_clusters"
    )
