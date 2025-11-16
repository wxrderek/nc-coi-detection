import pandas as pd
from matplotlib import pyplot as plt
import math

df1 = pd.read_csv("census_data.csv")
df2 = pd.read_csv("census_data_part_2.csv")



df = pd.concat([df1, df2], axis = 1)
df = df.loc[:, ~df.columns.duplicated()]



df = df.drop(columns = ["Total population (simple)", "Year structure built (categorical distribution)", "Household type by relationship", "Family households by presence of children", "Household type by age of householder", "Occupants per room (crowding)", "Household income distribution (total)", "Aggregate household income", "Educational attainment (detailed)", "Educational attainment total", "Field of bachelor's degree", "Occupants per room (crowding measure)", "School enrollment by type (public/private)"])



for column in df.columns:
    if df[column].isna().mean() * 100 >= 90:
        df = df.drop(columns=[column])

for col in df.columns[1:]:
    median = df[col].median()
    df[col] = df[col].mask(df[col] < 0, median)
    print(df[col].head())


    




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


df["16Pluspct"] = df["Population 16+"]/df["Total population"]
df["LaborForcepct"] = df["In labor force"]/df["Total population"]
df["Empolyedpct"] = df["Employed"]/df["Total population"]
df["Unemployedpct"] = df["Unemployed"]/df["Total population"]
df["NotInLaborForcepct"] = df["Not in labor force"]/df["Total population"]
df["MBSAOccpct"] = df["Management, business, science, arts occupations"]/df["Total population"]

df["25PlusEddAttpct"] = df["Educational attainment 25+"]/df["Total population"]
df["HighSchoolpct"] = df["High school graduate (includes equivalency)"]/df["Total population"]
df["1YearCollegePct"] = df["Some college, less than 1 year"]/df["Total population"]
df["1+YearCollegePct"] = df["Some college, 1+ years, no degree"]/df["Total population"]
df["Associatepct"] = df["Associate's degree"]/df["Total population"]
df["Bachelorpct"] = df["Bachelor's degree"]/df["Total population"]
df["Masterpct"] = df["Master's degree"]/df["Total population"]
df["ProfSchoolpct"] = df["Professional school degree"]/df["Total population"]
df["Doctoratepct"] = df["Doctorate degree"]/df["Total population"]

df["DriveAloneToWorkpct"] = df["Drive alone to work"]/df["Total population"]
df["PublicTransportToWorkpct"] = df["Public transportation to work"]/df["Total population"]
df["WalkedtoWorkpct"] = df["Walked to work"]/df["Total population"]
df["WorkedFromHomepct"] = df["Worked from home"]/df["Total population"]

df["18-24pct"] = df["Population age 18-24"]/df["Total population"]
df["25-34pct"] = df["Population age 25-34"]/df["Total population"]
df["Fem18-24pct"] = df["Female population 18-24"]/df["Total population"]




df = df.drop(columns = ["Total population", "Male population", "Female population", "White alone", "Black or African American alone", "Asian alone", "Hispanic or Latino origin", "Total housing units", "Occupied housing units", "Vacant housing units", "Owner-occupied housing units", "Renter-occupied housing units", "Vacant units for rent", "Vacant units for sale", "Total households", "Married-couple households", "Female householder, no husband present", "Male householder, no wife present", "Households with children under 18"])
df = df.drop(columns = ["Population 16+", "In labor force", "Civilian labor force", "Employed", "Unemployed", "Not in labor force", "Management, business, science, arts occupations", "Educational attainment 25+", "High school graduate (includes equivalency)", "Some college, less than 1 year", "Some college, 1+ years, no degree", "Associate's degree", "Bachelor's degree", "Master's degree", "Professional school degree", "Doctorate degree", "Drive alone to work", "Public transportation to work", "Mean travel time to work", "Walked to work", "Worked from home", "Population age 18-24", "Population age 25-34", "Female population 18-24", "Units in structure (1-unit, 2-unit, etc.)"])
#REMOVE NAs AND INFINITIES
for col in df.columns[1:]:
    if col == "GOID":
        continue
    median = df[col].median()
    df[col] = df[col].mask(df[col] > 10000000000000000, median)
    df[col] = df[col].mask(df[col].isna(), median)




df.to_csv("census_data_cleaned.csv")