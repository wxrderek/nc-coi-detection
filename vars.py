acs_variables = [
    # Population & Demographics
    "B01001_001E", "B01001_002E", "B01001_026E", "B01002_001E", "B01003_001E",
    "B01001A_001E", "B01001B_001E", "B01001D_001E", "B01001I_001E",
    "B02001_002E", "B02001_003E", "B02001_005E", "B03003_003E",
    "B05002_013E", "B07003_004E", "B07003_007E", "B07003_010E", "B07003_013E",
    "B09001_001E",

    # Housing
    "B25001_001E", "B25002_002E", "B25002_003E", "B25003_002E", "B25003_003E",
    "B25004_003E", "B25004_004E", "B25010_001E", "B25014_001E", "B25035_001E",
    "B25036_001E", "B25040_001E", "B25064_001E", "B25077_001E", "B25081_001E",
    "B25092_001E", "B25093_001E", "B25097_001E", "B25105_001E",
    "B25119_001E", "B25124_001E",

    # Family & Household
    "B11001_001E", "B11001_003E", "B11001_005E", "B11001_006E",
    "B11002_001E", "B11004_001E", "B11005_001E", "B11013_001E",
    "B11016_001E", "B11017_001E", "B11018_001E",

    # Income, Poverty & Employment
    "B19001_001E", "B19013_001E", "B19025_001E", "B19083_001E",
    "B19113_001E", "B19201_001E", "B19301_001E", "B17001_001E",
    "B17001_002E", "B23025_001E", "B23025_002E", "B23025_003E",
    "B23025_004E", "B23025_005E", "B23025_007E", "B24011_001E",
    "B24021_001E", "B24080_001E",

    # Education
    "B15001_001E", "B15002_001E", "B15003_001E", "B15003_017E",
    "B15003_018E", "B15003_019E", "B15003_020E", "B15003_021E",
    "B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E",
    "B15012_001E", "B16001_001E", "B16005_001E", "B16010_001E",
    "B16007_001E",

    # Nativity, Citizenship & Migration
    "B05001_001E", "B05002_001E", "B05006_001E", "B07001_001E",
    "B07003_001E", "B07204_001E", "B08301_001E", "B08301_003E",
    "B08301_010E", "B08303_001E",

    # Urbanicity & Commuting
    "B08301_019E", "B08301_021E", "B08406_001E", "B25044_001E",
    "B08119_001E",

    # Miscellaneous useful
    "B01001_020E", "B01001_021E", "B01001_028E", "B25015_001E",
    "B25024_001E", "B25034_001E", "B14001_001E", "B14002_001E",
    "B11012_001E"
]


acs_labels = {
    # Population & Demographics
    "B01001_001E": "Total population",
    "B01001_002E": "Male population",
    "B01001_026E": "Female population",
    "B01002_001E": "Median age",
    "B01003_001E": "Total population (simple)",
    "B01001A_001E": "White alone population",
    "B01001B_001E": "Black or African American alone population",
    "B01001D_001E": "Asian alone population",
    "B01001I_001E": "Hispanic or Latino population",
    "B02001_002E": "White alone",
    "B02001_003E": "Black or African American alone",
    "B02001_005E": "Asian alone",
    "B03003_003E": "Hispanic or Latino origin",
    "B05002_013E": "Foreign-born population",
    "B07003_004E": "Moved within same county last year",
    "B07003_007E": "Moved from different county (same state)",
    "B07003_010E": "Moved from different state",
    "B07003_013E": "Moved from abroad",
    "B09001_001E": "Population under 18 years",

    # Housing
    "B25001_001E": "Total housing units",
    "B25002_002E": "Occupied housing units",
    "B25002_003E": "Vacant housing units",
    "B25003_002E": "Owner-occupied housing units",
    "B25003_003E": "Renter-occupied housing units",
    "B25004_003E": "Vacant units for rent",
    "B25004_004E": "Vacant units for sale",
    "B25010_001E": "Average household size",
    "B25014_001E": "Occupants per room (crowding)",
    "B25035_001E": "Median year structure built",
    "B25036_001E": "Year structure built (categorical distribution)",
    "B25040_001E": "House heating fuel type",
    "B25064_001E": "Median gross rent",
    "B25077_001E": "Median home value",
    "B25081_001E": "Tenure by household income",
    "B25092_001E": "Mortgage status",
    "B25093_001E": "Owner costs as % of income",
    "B25097_001E": "Mortgage status & owner costs",
    "B25105_001E": "Median monthly owner costs (with mortgage)",
    "B25119_001E": "Tenure by household size",
    "B25124_001E": "Tenure by presence of children",

    # Family & Household
    "B11001_001E": "Total households",
    "B11001_003E": "Married-couple households",
    "B11001_005E": "Female householder, no husband present",
    "B11001_006E": "Male householder, no wife present",
    "B11002_001E": "Household type by relationship",
    "B11004_001E": "Family households by presence of children",
    "B11005_001E": "Households with children under 18",
    "B11013_001E": "Subfamilies",
    "B11016_001E": "Household type by age of householder",
    "B11017_001E": "Household type by household size",
    "B11018_001E": "Households by people under 18 and 65+",

    # Income, Poverty & Employment
    "B19001_001E": "Household income distribution (total)",
    "B19013_001E": "Median household income",
    "B19025_001E": "Aggregate household income",
    "B19083_001E": "Gini index of income inequality",
    "B19113_001E": "Median family income",
    "B19201_001E": "Per capita income",
    "B19301_001E": "Per capita income (individuals)",
    "B17001_001E": "Population for whom poverty status determined",
    "B17001_002E": "Below poverty level",
    "B23025_001E": "Population 16+",
    "B23025_002E": "In labor force",
    "B23025_003E": "Civilian labor force",
    "B23025_004E": "Employed",
    "B23025_005E": "Unemployed",
    "B23025_007E": "Not in labor force",
    "B24011_001E": "Median earnings by industry",
    "B24021_001E": "Occupation by sex",
    "B24080_001E": "Management, business, science, arts occupations",

    # Education
    "B15001_001E": "Educational attainment by sex",
    "B15002_001E": "Educational attainment 25+",
    "B15003_001E": "Educational attainment (detailed)",
    "B15003_017E": "High school graduate (includes equivalency)",
    "B15003_018E": "Some college, less than 1 year",
    "B15003_019E": "Some college, 1+ years, no degree",
    "B15003_020E": "Associate's degree",
    "B15003_021E": "Bachelor's degree",
    "B15003_022E": "Master's degree",
    "B15003_023E": "Professional school degree",
    "B15003_024E": "Doctorate degree",
    "B15003_025E": "Educational attainment total",
    "B15012_001E": "Field of bachelor's degree",
    "B16001_001E": "Language spoken at home",
    "B16005_001E": "Language by English proficiency",
    "B16010_001E": "Language by age",
    "B16007_001E": "Place of birth by language spoken",

    # Nativity, Citizenship & Migration
    "B05001_001E": "Citizenship status",
    "B05002_001E": "Place of birth (total)",
    "B05006_001E": "Place of birth for foreign-born",
    "B07001_001E": "Geographical mobility (pop 1+ year)",
    "B07003_001E": "Moved residence in past year (total)",
    "B07204_001E": "Travel time to work",
    "B08301_001E": "Means of transportation to work",
    "B08301_003E": "Drive alone to work",
    "B08301_010E": "Public transportation to work",
    "B08303_001E": "Mean travel time to work",

    # Urbanicity & Commuting
    "B08301_019E": "Walked to work",
    "B08301_021E": "Worked from home",
    "B08406_001E": "Workers by vehicle availability",
    "B25044_001E": "Tenure by vehicles available",
    "B08119_001E": "Transportation to work by household income",

    # Miscellaneous useful
    "B01001_020E": "Population age 18-24",
    "B01001_021E": "Population age 25-34",
    "B01001_028E": "Female population 18-24",
    "B25015_001E": "Occupants per room (crowding measure)",
    "B25024_001E": "Units in structure (1-unit, 2-unit, etc.)",
    "B25034_001E": "Year structure built (categorical)",
    "B14001_001E": "School enrollment by level",
    "B14002_001E": "School enrollment by type (public/private)",
    "B11012_001E": "Households by household type (family/nonfamily)"
}
