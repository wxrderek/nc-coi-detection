from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import networkx as nx
import numpy as np
from scipy.sparse import load_npz
import igraph as ig
import leidenalg
import matplotlib.pyplot as plt
import geopandas as gpd
from libpysal.weights import W
from spopt.region import WardSpatial
from shapely.geometry import Point




G = nx.Graph()

pca_data = np.load("census_data_pca.npz")
geoids = pca_data["geoids"]
pca_matrix = pca_data["pca"]




for i, geoid in enumerate(geoids):
    G.add_node(i, geoid = geoid, pcs = pca_matrix[i])

# pca_matrix: shape (N, 6)
N = pca_matrix.shape[0]

df = pd.DataFrame(pca_matrix, columns=[f"PC{i+1}" for i in range(6)])

# Dummy geometry (a requirement for GeoDataFrame)
df["geometry"] = [Point(0, 0)] * N

gdf = gpd.GeoDataFrame(df, geometry="geometry")

adj_matrix = load_npz("../Adjacency/nc-bg-adjacency.npz")
rows, cols = adj_matrix.nonzero()


# adjacency list dict: i -> list of neighbors
adj_dict = {}
N = adj_matrix.shape[0]

for i in range(N):
    adj_dict[i] = []

for u, v in zip(rows, cols):
    if u != v:
        adj_dict[u].append(v)

# Create PySAL contiguity object
W_adj = W(adj_dict)


K = 550   # <-- choose your desired number of COIs

model = WardSpatial(gdf, W_adj, attrs_name=[f"PC{i+1}" for i in range(6)],  n_clusters=K)
model.solve()

ward_labels = np.array(model.labels_)

df_coi_ward = pd.DataFrame({
    "GEOID": geoids.astype(str),
    "COI_Ward": ward_labels
})


edges = [(int(r), int(c)) for r, c in zip(rows, cols) if r < c]

G.add_edges_from(edges)

for u, v in edges:
    sim = cosine_similarity(
        pca_matrix[u].reshape(1, -1),
        pca_matrix[v].reshape(1, -1)
    )[0, 0]
    G[u][v]['weight'] = (sim + 1)/2

g_ig = ig.Graph.from_networkx(G)

partition = leidenalg.find_partition(
    g_ig,
    leidenalg.RBConfigurationVertexPartition,
    weights="weight",
    resolution_parameter=80
)

leiden_labels = partition.membership  # list of cluster IDs

print(np.unique(leiden_labels))



df_coi = pd.DataFrame({
    "GEOID": geoids.astype(str),
    "COI_Leiden": leiden_labels
})

    
shp = gpd.read_file("shapefiles/nc_bg/tl_2023_37_bg.shp")

shp = shp.merge(df_coi, on="GEOID", how="left")


fig, ax = plt.subplots(figsize=(10, 14))
shp.plot(column="COI_Leiden",
         cmap="plasma",
         linewidth=0,
         ax=ax,
         legend = False)
ax.axis("off")
plt.title("NC Census Block Group COIs (Leiden)")
plt.savefig("Images/COIS/Leiden_COIS_geomap.png")

shp = gpd.read_file("shapefiles/nc_bg/tl_2023_37_bg.shp")

shp = shp.merge(df_coi_ward, on="GEOID", how="left")

fig, ax = plt.subplots(figsize=(10, 14))
shp.plot(column="COI_Ward",
         cmap="magma",
         linewidth=0,
         ax=ax,
         legend = False)
ax.axis("off")
plt.title("NC Census Block Group COIs (Ward)")
plt.savefig("Images/COIS/Ward_COIS_geomap.png")





# # Use a force-directed layout (Fruchterman–Reingold)
# pos = nx.spring_layout(G, weight='weight', seed=42)

# # Extract Leiden labels
# labels = leiden_labels

# # Draw
# plt.figure(figsize=(12, 12))
# nx.draw_networkx_nodes(G, pos, node_size=15, node_color=labels, cmap='tab20')
# nx.draw_networkx_edges(G, pos, alpha=0.1, width=0.2)

# plt.title("Leiden COI Structure (Topology-only Visualization)")
# plt.axis("off")
# plt.savefig("leiden_COIS.png")





