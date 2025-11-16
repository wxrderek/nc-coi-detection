from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pandas as pd

X = pd.read_csv("../Census\ Data/census_data.csv")

variables = X.columns

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


pca = PCA(n_components=6)
X_pca = pca.fit_transform(X_scaled)

loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f"PC{i+1}" for i in range(6)],
    index=variables
)

pc1_contrib = loadings["PC1"].abs().sort_values(ascending=False)
print(pc1_contrib.head(10))
