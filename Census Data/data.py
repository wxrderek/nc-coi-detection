import requests
import pandas as pd
from time import sleep



API = "e1dc566c4bf0a8c72117cc9b7deda7fadc0e75bf"
BASE = "https://api.census.gov/data/2023/acs/acs5"



VARIABLES = [
    "NAME",
    # --- RACE & ETHNICITY ---
    "B02001_001E",  # Total population
    "B03002_003E",  # Hispanic or Latino
    "B02001_002E",  # White alone
    "B02001_003E",  # Black or African American alone
    "B02001_005E",  # Asian alone
    "B02001_006E",  # Native Hawaiian / Pacific Islander

    # --- SOCIOECONOMIC ---
    "B19013_001E",  # Median household income
    "B17001_002E",  # Below poverty level
    "B15003_022E",  # Bachelor's degree or higher

    # --- HOUSING ---
    "B25064_001E",  # Median gross rent
    "B25077_001E",  # Median home value
    "B25001_001E",  # Total housing units

    # --- LANGUAGE ---
    "C16001_002E",  # Speak Spanish at home
    "C16001_003E",  # Other Indo-European languages at home

    # --- AGE ---
    "B01001_020E",  # Age 20–34 (Male 20–24 — good proxy for young adults)

    # --- BONUS VARIABLES ---
    "B08301_001E",  # Means of transportation to work (total workers)
    "DP03_0025E",   # Mean travel time to work (minutes)
    "B11001_001E",  # Total households
    "B25044_003E",  # Heating fuel: electricity (common rural/urban indicator)
]


variable_names = {
    # --- RACE & ETHNICITY ---
    "B02001_001E": "Total population",
    "B03002_003E": "Hispanic or Latino population",
    "B02001_002E": "White alone",
    "B02001_003E": "Black or African American alone",
    "B02001_005E": "Asian alone",
    "B02001_006E": "Pacific Islander or Native Hawaiian alone",

    # --- SOCIOECONOMIC ---
    "B19013_001E": "Median household income",
    "B17001_002E": "Population below poverty level",
    "B15003_022E": "Educational attainment: Bachelor's degree or higher",

    # --- HOUSING ---
    "B25064_001E": "Median gross rent",
    "B25077_001E": "Median home value",
    "B25001_001E": "Total housing units",

    # --- LANGUAGE ---
    "C16001_002E": "Speak Spanish at home",
    "C16001_003E": "Speak other Indo-European languages at home",

    # --- AGE ---
    "B01001_020E": "Young adult population (age ~20–34 proxy)",

    # --- BONUS VARIABLES ---
    "B08301_001E": "Total workers (commuting base)",
    "DP03_0025E": "Mean travel time to work (minutes)",
    "B11001_001E": "Total households",
    "B25044_003E": "Heating fuel: electricity (proxy for rural/urban divide)",
}


get_vars = ",".join(VARIABLES)


# First: get all tracts in NC
tract_url = (
    f"{BASE}?get=NAME&for=tract:*&in=state:37&key={API}"
)

tracts = requests.get(tract_url).json()[1:]


rows = []

i = 0

for name, state, county, tract in tracts:
    print(f"Tract {i} out of {len(tracts)}")
    # Now query all block groups inside this tract
    bg_url = (
        f"{BASE}?get={get_vars}"
        f"&for=block%20group:*"
        f"&in=state:37+county:{county}+tract:{tract}"
        f"&key={API}"
    )
    #GOID: State + County + Tract + Block Number
    data = requests.get(bg_url).json()[1:]
    for row in data:
        row[0] = row[0].split("; ")[2]
        rows.append(row)
    sleep(0.15)  # avoid rate limits

    i += 1

# Convert to dataframe
columns = VARIABLES + ["state", "county", "tract", "block_group"]
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
