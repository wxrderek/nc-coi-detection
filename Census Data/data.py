import requests
import pandas as pd

API = "e1dc566c4bf0a8c72117cc9b7deda7fadc0e75bf"
BASE = "https://api.census.gov/data/2023/acs/acs5"

VARIABLES = ["NAME", "B01003_001E"]  # total population
get_vars = ",".join(VARIABLES)

# First: get all tracts in NC
tract_url = (
    f"{BASE}?get=NAME&for=tract:*&in=state:37&key={API}"
)

tracts = requests.get(tract_url).json()[1:]

rows = []

for name, state, county, tract in tracts:
    # Now query all block groups inside this tract
    bg_url = (
        f"{BASE}?get={get_vars}"
        f"&for=block%20group:*"
        f"&in=state:37+county:{county}+tract:{tract}"
        f"&key={API}"
    )

    data = requests.get(bg_url).json()[1:]
    for row in data:
        rows.append(row)

# Convert to dataframe
columns = VARIABLES + ["state", "county", "tract", "block_group"]
df = pd.DataFrame(rows, columns=columns)

print(df.head())
print("Total NC block groups:", len(df))
