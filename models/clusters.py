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
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns


    clusters = {}
    for i, label in enumerate(cluster_labels):
        clusters.setdefault(label, []).append(i)

    # Calculate average pairwise distances between clusters
    cluster_dist = np.zeros((num_clusters, num_clusters))
    for i in range(1, num_clusters + 1):
        for j in range(1, num_clusters + 1):
            pts_i = clusters[i]
            pts_j = clusters[j]
            dists = pairwise_distance_matrix[np.ix_(pts_i, pts_j)]
            cluster_dist[i - 1, j - 1] = np.mean(dists)

    # # Print formatted matrix
    # print("\nFormatted Distances Between Clusters:")
    # for i in range(cluster_dist.shape[0]):
    #     for j in range(cluster_dist.shape[1]):
    #         print(f"Cluster {i+1}, Cluster {j+1}: {cluster_dist[i, j]:.2f}")


    if show:
        plt.figure(figsize=(10, 8))
        sns.heatmap(cluster_dist, cmap='Purples', annot=True)
        plt.title("Average Distance Between Clusters")
        plt.xlabel("Cluster")
        plt.ylabel("Cluster")
        plt.show()

    return cluster_dist

def clusters_hierarchy(pairwise_distance_matrix, num_clusters, cluster_labels, idxmap,
                       cluster_dist, plotly_img=True, save_geojson_path=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import rasterio.features
    from rasterio.transform import Affine
    from shapely.geometry import shape
    import geopandas as gpd
    import plotly.express as px

    # --- Compute intra-cluster distances (cohesion) ---
    intra_cluster_dists = {}
    for label in range(1, num_clusters + 1):
        pts = np.where(cluster_labels == label)[0]
        if len(pts) > 1:
            submatrix = pairwise_distance_matrix[np.ix_(pts, pts)]
            mean_dist = np.mean(submatrix)
        else:
            mean_dist = 0
        intra_cluster_dists[label] = mean_dist

    # --- Build cohesion map (2D grid) ---
    cohesion_map = np.full((lsmc.shape[0] * lsmc.shape[1]), np.nan)
    active_region_indices = np.flatnonzero(lsmc.flatten() == 1)
    for i, ind in enumerate(active_region_indices):
        cluster_label = cluster_labels[i]
        cohesion_map[ind] = intra_cluster_dists[cluster_label]
    cohesion_map = cohesion_map.reshape(lsmc.shape)

    # --- Label positions for overlay ---
    label_positions = {}
    lat_vals = lsmdf.latitude.values
    lon_vals = lsmdf.longitude.values
    for label in range(1, num_clusters + 1):
        mask = (idxmap == label)
        if np.any(mask):
            y_idx, x_idx = np.where(mask)
            cluster_lats = lat_vals[y_idx]
            cluster_lons = lon_vals[x_idx]
            lat_center = np.mean(cluster_lats)
            lon_center = np.mean(cluster_lons)
            label_positions[label] = (lon_center, lat_center)

    # --- Static cohesion map ---
    plt.figure(figsize=(10, 8))
    plt.pcolor(lsmdf.longitude, lsmdf.latitude, cohesion_map,
               cmap='viridis', shading='auto', rasterized=True)
    plt.colorbar(label='Cluster Cohesion (lower = tighter)')
    plt.title("Cluster Cohesion Map with Labels")
    for label, (lon, lat) in label_positions.items():
        plt.text(lon, lat, str(label), ha='center', va='center',
                 fontsize=9, fontweight='bold', color='white',
                 bbox=dict(facecolor='black', alpha=0.5, boxstyle='round'))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.show()

    # --- Optional Plotly map + GeoJSON export ---
    if plotly_img:
        res_lat = lat_vals[1] - lat_vals[0]
        res_lon = lon_vals[1] - lon_vals[0]
        transform = Affine.translation(lon_vals[0] - res_lon / 2, lat_vals[0] - res_lat / 2) * Affine.scale(res_lon, res_lat)

        # Build label grid for polygonization
        label_grid = np.full(lsmc.shape, -1)
        for i, ind in enumerate(active_region_indices):
            label_grid[np.unravel_index(ind, lsmc.shape)] = cluster_labels[i]

        # Polygonize
        shapes_gen = rasterio.features.shapes(label_grid.astype(np.int32), transform=transform)
        geoms = []
        cluster_ids = []
        cohesions = []
        inter_dists = []

        for geom, cluster_id_raw in shapes_gen:
            cluster_id = int(cluster_id_raw)
            if cluster_id == -1:
                continue
            geoms.append(shape(geom))
            cluster_ids.append(cluster_id)
            cohesions.append(float(intra_cluster_dists[cluster_id]))
            dist_dict = {
                str(j + 1): float(cluster_dist[cluster_id - 1, j])
                for j in range(num_clusters) if j + 1 != cluster_id
            }
            inter_dists.append(dist_dict)

        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame({
            'cluster_id': cluster_ids,
            'cohesion': cohesions,
            'distances': inter_dists
        }, geometry=geoms)
        gdf.set_crs(epsg=4326, inplace=True)
        gdf = gdf.dissolve(by='cluster_id', as_index=False, aggfunc='first')

        # Plotly map
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

        # Export GeoJSON with all metadata
        if save_geojson_path:
            gdf.to_file(f"{save_geojson_path}/clusters_cohesion.geojson", driver='GeoJSON')



if __name__ == "__main__":
    data_path = "../data/raw"
    loader = DataLoader(data_path)
    lsmdf, lsmc, rlsmcs5Wmnavg = loader.load_wind_correlation_data()
    pairwise_distance_matrix, num_clusters, cluster_labels, idxmap = hierarchical_clustering(lsmdf, lsmc,
                                                                                             rlsmcs5Wmnavg, show=True)
    cluster_dist = distance_matrix(pairwise_distance_matrix,
                    num_clusters, cluster_labels, show=True)
    clusters_hierarchy(pairwise_distance_matrix, num_clusters,
                       cluster_labels, idxmap, save_geojson_path="../data/processed", cluster_dist=cluster_dist)



