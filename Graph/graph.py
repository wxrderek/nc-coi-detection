from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import networkx as nx
import numpy as np
from scipy.sparse import load_npz
import igraph as ig
import leidenalg
import matplotlib.pyplot as plt

G = nx.Graph()

pca_data = np.load("census_data_pca.npz")
geoids = pca_data["geoids"]
pca_matrix = pca_data["pca"]




for i, geoid in enumerate(geoids):
    G.add_node(i, geoid = geoid, pcs = pca_matrix[i])

adj_matrix = load_npz("../Adjacency/nc-bg-adjacency.npz")
rows, cols = adj_matrix.nonzero()
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
    resolution_parameter=1.0
)

leiden_labels = partition.membership  # list of cluster IDs


# Use a force-directed layout (Fruchterman–Reingold)
pos = nx.spring_layout(G, weight='weight', seed=42)

# Extract Leiden labels
labels = leiden_labels

# Draw
plt.figure(figsize=(12, 12))
nx.draw_networkx_nodes(G, pos, node_size=15, node_color=labels, cmap='tab20')
nx.draw_networkx_edges(G, pos, alpha=0.1, width=0.2)

plt.title("Leiden COI Structure (Topology-only Visualization)")
plt.axis("off")
plt.savefig("leiden_COIS.png")





