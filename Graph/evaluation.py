import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

population = pd.read_csv("../Census Data/census_data.csv")[["GOID", "Total population"]].rename(columns = {"GOID": "GEOID"})
district_mapping = pd.read_csv("../Map/bg_to_cd_mapping.csv").rename(columns = {"BG_GEOID": "GEOID"})
coi_mapping = pd.read_csv("coi_mapping.csv")
block_voting = pd.read_csv("../Census Data/bg-vote-percentage-new.csv").rename(columns = {"bg_GEOID": "GEOID"})[["GEOID", "avg_pct_dem", "avg_pct_rep"]]



df = pd.concat([population, district_mapping, coi_mapping, block_voting], axis = 1).drop(columns=["Unnamed: 0"])
df = df.loc[:, ~df.columns.duplicated()]


  # ----------------------------------------------------
    # Step 1: Convert percentages → estimated vote totals
    # ----------------------------------------------------
df["votes_dem"] = df["avg_pct_dem"] * df["Total population"]
df["votes_rep"] = df["avg_pct_rep"] * df["Total population"]

# ----------------------------------------------------
# Step 2: Compute district-level vote outcomes
# ----------------------------------------------------
district_votes = df.groupby("CD").agg(
    dem_total=("votes_dem", "sum"),
    rep_total=("votes_rep", "sum")
)

district_votes["district_vote"] = (
    district_votes["dem_total"] > district_votes["rep_total"]
).astype(int)

district_vote_map = district_votes["district_vote"].to_dict()

# ----------------------------------------------------
# Step 3: Compute fragment-level (COI × district) votes
# ----------------------------------------------------
fragments = df.groupby(["COI_Ward", "CD"]).agg(
    frag_dem=("votes_dem", "sum"),
    frag_rep=("votes_rep", "sum"),
    frag_pop=("Total population", "sum")
)

fragments["vote_frag"] = (fragments["frag_dem"] > fragments["frag_rep"]).astype(int)

def compute_residual(row):
    district_id = row.name[1]
    frag_vote = row["vote_frag"]
    district_vote = district_vote_map[district_id]

    # indicator mismatch * population of the fragment
    return row["frag_pop"] if frag_vote != district_vote else 0

fragments["R"] = fragments.apply(compute_residual, axis=1)

# ----------------------------------------------------
# Step 5: Compute COI-level loss L(C)
# ----------------------------------------------------
coi_pop = df.groupby("COI_Ward")["Total population"].sum()
coi_residual = fragments.groupby("COI_Ward")["R"].sum()

L = (coi_residual / coi_pop).fillna(0)

print(L.mean())

# plt.hist(L)
# plt.show()






