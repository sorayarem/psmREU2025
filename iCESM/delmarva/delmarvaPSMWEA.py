## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import os
import argparse
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from delmarvaOxyIso import d18OAnoms
from delmarvaAnnualAnomalies import iCESMAnnualAnoms
from delmarvaExpertAnomalies import iCESMExpertAnoms
from openpyxl import load_workbook
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

## setting up the model arugments
parser = argparse.ArgumentParser(description='Running PSM...')
parser.add_argument('--season', type=int, choices=[0, 1], default=0, help='Seasonal preference (0 = Annual, 1 = Expert)')
parser.add_argument('--model', type=int, choices=[1, 2, 3], default=1, help='Model preference (1=Temp, 2=Salinity, 3=Both)')
parser.add_argument('--iso', type=int, choices=[0, 1], default=1, help='Isotope preference (0 = Salt-Enabled, 1 = Isotope-Enabled)')
args = parser.parse_args()

## setting the seasonal preference (F:Annual; T:Expert)
season = args.season

## setting the model preference (1: Temperature; 2:Salinity, 3:Both)
model = args.model

## setting the isotope preference (F:Salt-Enabled; T:Isotope-Enabled)
isotope = args.iso

## building the pseudocarbonate
def pseudocarbonate(SST, SSS, ISO):
    ## define a1 and a2 based on the region (north atlantic)
    a1 = 0.22
    a2 = 0.97002 * ISO if isotope else 0.97002 * 0.55

    ## calculating pseudocarbonate value
    if(isotope):
        carbonate = a1 * SST + a2 if model == 3 else (a1 * SST if model == 1 else a2)
    else:
        carbonate = a1 * SST + a2 * SSS if model == 3 else (a1 * SST if model == 1 else a2 * SSS)
    return carbonate

## finding the years that are in both datasets
iCESMYears = iCESMExpertAnoms['year'] if season else iCESMAnnualAnoms['year']
d18OYears = d18OAnoms['year']

intersect = np.intersect1d(iCESMYears, d18OYears)

## only keeping the overlapping years
iCESMFiltered = iCESMExpertAnoms.sel(year = intersect) if season else iCESMAnnualAnoms.sel(year = intersect)
d18OFiltered = d18OAnoms[d18OAnoms['year'].isin(intersect)]

d18OXRArray = xr.DataArray(
    d18OFiltered['d18OAnoms'].values,
    coords={'year': d18OFiltered['year'].values},
    dims='year',
    name='d18OAnoms'
)

## merge (based on the year)
merged = iCESMFiltered.copy()
merged['d18OAnoms'] = d18OXRArray 
df = merged.to_dataframe().reset_index()

## computing the pseudocarbonate for each year
if {'year', 'temp', 'salt', 'iso'}.issubset(df.columns):
    pseudocarbonateData = []
    for _, row in df.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['temp'],
            SSS=row['salt'],
            ISO=row['iso'])
        pseudocarbonateData.append(pseudoCarbonateValue)

    ## converting to a data frame
    merged['pseudocarbonate'] = pseudocarbonateData
    data = merged
else:
    print("Missing required columns in overlapping_df")

## plotting the results of the PSM
plt.figure(figsize=(12, 6))

## plotting the timeseries
plt.plot(data['year'], data['d18OAnoms'], label='shell record', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')
plt.xlabel('Year')
plt.ylabel('Anomaly Value')

## plotting the correlation
##plt.scatter(data['d18OAnoms'], data['pseudocarbonate'], label='d18OAnoms', color='#008080')

filepath = "./figures/icesm"
if isotope:
    figname = "delmarva_iCESM_WEA_M" + str(model) + "(I)_" + ("EXP" if season else "ANN") + ".png"
else:
    figname = "delmarva_iCESM_WEA_M" + str(model) + "(S)_" + ("EXP" if season else "ANN") + ".png"
filename = os.path.join(filepath, figname)


plt.suptitle('Delmarva Shelf', fontsize = 16, fontweight = 'bold')
method = "Williams et al. Method (Expert Season)" if season else "Williams et al. Method (Annual Season)"
if isotope:
    modelType = "Temperature + Isotopes" if model == 3 else ("Temperature Only" if model == 1 else "Isotopes Only")
else:
    modelType = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + modelType)
plt.legend()
plt.grid(True)
plt.savefig(filename)

# creating the merged data frame
df = pd.DataFrame({ 'year': data['year'], 'observed': data['d18OAnoms'], 'pseudocarb': data['pseudocarbonate']})

# dropping rows where either observed or pseudocarb is n/a
filter = df.dropna(subset=['observed', 'pseudocarb'])
observed = filter['observed']
pseudocarb = filter['pseudocarb']
years = filter['year']

## finding correlation coefficient (r) and the p-value
r, sig, pValue = corr_isopersist(observed, pseudocarb)
print("Correlation:", r)
print("p-value:", pValue)

## finding root mean squared error
rmse = np.sqrt(((filter['observed'] - filter['pseudocarb']) ** 2).mean())
print("RMSE:", rmse.item())

## finding null-model root mean squared error
nrmse = np.sqrt(((0 - filter['observed']) ** 2).mean())
print("NRMSE:", nrmse.item())

## saving the results to an excel file
file = "psmREUStats.xlsx"
site = "Delmarva Shelf"
equation = "WEA"
data = "iCESM"
season = "Expert" if season else "Annual"
if(isotope):
    method = "Both(I)" if model == 3 else ("Temperature(I)" if model == 1 else "Isotopes")
else:
    method = "Both(S)" if model == 3 else ("Temperature(S)" if model == 1 else "Salinity")

modelResults = {'Site': site, 'Data': data,'Season': season, 'Method': method, 'Equation': equation}

modelResults['r'] = r
modelResults['p-value'] = pValue
modelResults['RMSE'] = rmse.item()
modelResults['NRMSE'] = nrmse.item()

rowToAdd = pd.DataFrame([modelResults])

if os.path.exists(file):
    ## loading the excel file
    previousDF = pd.read_excel(file)

    ## checking if the same row already exists
    match = ((previousDF['Site'] == site) & (previousDF['Data'] == data) & (previousDF['Season'] == season) & 
                (previousDF['Method'] == method) & (previousDF['Equation'] == equation))

    if match.any():
        ## replacing the existing row
        previousDF.loc[match, :] = rowToAdd.values[0]
        print("Row already exists, overwriting file...")
    else:
        ## adding the new row
        previousDF = pd.concat([previousDF, rowToAdd], ignore_index=True)
        print("Row doesn't exist, adding...")

    ## saving the changes to excel
    with pd.ExcelWriter(file, engine='openpyxl', mode='w') as writer:
        previousDF.to_excel(writer, index=False)
else:
    ## creating a new file
    rowToAdd.to_excel(file, index=False, engine='openpyxl')

print("Row added!")
