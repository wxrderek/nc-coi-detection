from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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

pc1_contrib = loadings["PC1"].abs().sort_values(ascending=False)
print(pc1_contrib.head(10))
