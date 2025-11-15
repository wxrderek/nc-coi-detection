import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

# --- Step 1: Load your edges file ---
edges = pd.read_csv("nc-bg-edges.csv")

# Make sure columns are named consistently
edges.columns = ["src", "dst"]

# --- Step 2: Get all unique block group IDs ---
all_ids = pd.Index(np.unique(edges[["src", "dst"]].values))
n = len(all_ids)
print(f"{n} unique block groups found")

# --- Step 3: Map block group IDs to matrix indices ---
id_to_idx = pd.Series(range(n), index=all_ids)

# --- Step 4: Build row/col index arrays for sparse matrix ---
rows = edges["src"].map(id_to_idx)
cols = edges["dst"].map(id_to_idx)

# --- Step 5: Create an undirected adjacency (symmetric) ---
data = np.ones(len(edges))
adjacency = coo_matrix((data, (rows, cols)), shape=(n, n))

# Make symmetric (if your graph is undirected)
adjacency = adjacency + adjacency.T

# Remove self-loops (optional)
adjacency.setdiag(0)
adjacency.eliminate_zeros()

# --- Step 6: Convert to CSR for efficient operations ---
adjacency = adjacency.tocsr()

print(adjacency.shape, "nonzero entries:", adjacency.nnz)

# --- Optional: save for later use ---
from scipy.sparse import save_npz
save_npz("nc-bg-adjacency.npz", adjacency)

# --- Optional: save the ID index mapping ---
all_ids.to_series().to_csv("nc-bg-index.csv", index_label="matrix_index", header=["block_group"])
