import requests
import pandas as pd
from time import sleep
import json

import vars



API = "e1dc566c4bf0a8c72117cc9b7deda7fadc0e75bf"
BASE = "https://api.census.gov/data/2023/acs/acs5"



VARIABLES = vars.VARIABLES

LABELS = vars.LABELS





get_vars = ",".join(VARIABLES)


# First: get all tracts in NC
tract_url = (
    f"{BASE}?get=NAME&for=tract:*&in=state:37&key={API}"
)

tracts = requests.get(tract_url).json()[1:]


rows = []

def safe_json_request(url, retries=3, delay=0.15):
    for attempt in range(retries):
        r = requests.get(url)
        try:
            return r.json()
        except json.JSONDecodeError:
            # Try again after a delay
            if attempt < retries - 1:
                sleep(delay)
            else:
                print("\n⚠️ JSON decode failed for URL:", url)
                print("Response preview:", r.text[:300])
                return None


for i, (name, state, county, tract) in enumerate(tracts, start=1):
    print(f"Tract {i} out of {len(tracts)}")
    # Now query all block groups inside this tract
    bg_url = (
        f"{BASE}?get={get_vars}"
        f"&for=block%20group:*"
        f"&in=state:37+county:{county}+tract:{tract}"
        f"&key={API}"
    )
    #GOID: State + County + Tract + Block Number
    data = safe_json_request(bg_url)
    if data is None:
        continue  # Skip this tract and avoid crashing
    data = data[1:]
    for row in data:
        row[0] = row[0].split("; ")[2]
        rows.append(row)

# Convert to dataframe
COLNAMES = [LABELS[var] for var in VARIABLES]
columns = COLNAMES + ["state", "county", "tract", "block_group"]
df = pd.DataFrame(rows, columns=columns)
df["GOID"] = (
    df["state"].astype(str)
    + df["county"].astype(str)
    + df["tract"].astype(str)
    + df["block_group"].astype(str)
)

print(df.head())
print("Total NC block groups:", len(df))

df.to_csv("census_data.csv", index = False)
