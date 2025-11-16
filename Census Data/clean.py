import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("census_data.csv")

df = df.drop(columns = ["Total population (simple)", "Year structure built (categorical distribution)", "Household type by relationship", "Family households by presence of children", "Household type by age of householder", "Occupants per room (crowding)"])



for column in df.columns:
    if df[column].isna().mean() * 100 >= 90:
        df = df.drop(columns=[column])

for col in df.columns[1:]:
    median = df[col].median()
    df[col] = df[col].mask(df[col] < 0, median)




df["Malepct"] = df["Male population"]/df["Total population"]
df["Femalepct"] = df["Female population"]/df["Total population"]
df["Whitepct"] = df["White alone"]/df["Total population"]
df["AfricanAmericanpct"] = df["Black or African American alone"]/df["Total population"]
df["Asianpct"] = df["Asian alone"]/df["Total population"]
df["Hispanicpct"] = df["Hispanic or Latino origin"]/df["Total population"]

df["TotHousingUnitspct"] = df["Total housing units"]/df["Total population"]
df["OccHousingUnitspct"] = df["Occupied housing units"]/df["Total housing units"]
df["VacHousingUnitspct"] = df["Vacant housing units"]/df["Total housing units"]
df["OwnerOccHousingUnitspct"] = df["Owner-occupied housing units"]/df["Occupied housing units"]
df["RenterOccHousingUnitspct"] = df["Renter-occupied housing units"]/df["Occupied housing units"]
df["VacUnitsForRentpct"] = df["Vacant units for rent"]/df["Vacant housing units"]
df["VacUnitsForSalepct"] = df["Vacant units for sale"]/df["Vacant housing units"]

df["TotHouseholdspct"] = df["Total households"]/df["Total population"]
df["MarriedCoupleHouseholdspct"] = df["Married-couple households"]/df["Total households"]
df["SoloFemaleHouseholdpct"] = df["Female householder, no husband present"]/df["Total households"]
df["SoloMaleHouseholdpct"] = df["Male householder, no wife present"]/df["Total households"]
df["HouseholdsWithChildrenpct"] = df["Households with children under 18"]/df["Total households"]
# print(df["Total population"].head())

df = df.drop(columns = ["Total population", "Male population", "Female population", "White alone", "Black or African American alone", "Asian alone", "Hispanic or Latino origin", "Total housing units", "Occupied housing units", "Vacant housing units", "Owner-occupied housing units", "Renter-occupied housing units", "Vacant units for rent", "Vacant units for sale", "Total households", "Married-couple households", "Female householder, no husband present", "Male householder, no wife present", "Households with children under 18"])


df.to_csv("census_data_cleaned.csv")