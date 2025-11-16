from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np

df = pd.read_csv("../Census Data/census_data_cleaned.csv")




X = df.drop(columns = ["NAME", "state", "county", "tract", "GOID"])



GEOIds = df["GOID"]
print(GEOIds)

variables = X.columns

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


pca = PCA(n_components=6)
X_pca = pca.fit_transform(X_scaled)



np.savez("census_data_pca.npz", geoids = df["GOID"].values, pca=X_pca)


loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f"PC{i+1}" for i in range(6)],
    index=variables
)



# plt.figure(figsize=(8, 5))
# plt.plot(
#     range(1, len(pca.explained_variance_ratio_) + 1),
#     pca.explained_variance_ratio_,
#     marker='o'
# )
# plt.xlabel("Principal Component")
# plt.ylabel("Explained Variance Ratio")
# plt.title("Scree Plot")
# plt.grid(True)
# plt.savefig("PCAScree.png")

pc1 = loadings["PC1"].abs().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
pc1.plot(kind="bar")

plt.title("Variable Contributions to Principal Component 1")
plt.xlabel("Variable")
plt.ylabel("Absolute Loading Value")
plt.tight_layout()
plt.savefig("PCA1Contributions.png")

