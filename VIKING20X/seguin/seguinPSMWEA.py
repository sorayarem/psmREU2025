## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import os
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from seguinOxyIso import d18OAnoms
from seguinAnnualAnomalies import vikingAnnualAnoms
from seguinExpertAnomalies import vikingExpertAnoms
from openpyxl import load_workbook
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

## setting the seasonal preference (F:Annual; T:Expert)
season = False

## setting the model preference (1: Temperature; 2:Salinity, 3:Both)
model = 3

## building the pseudocarbonate
def pseudocarbonate(SST, SSS):
    ## define a1 and a2 based on the region (north atlantic)
    a1 = 0.22
    a2 = 0.97002 * 0.55

    ## calculating pseudocarbonate value
    carbonate = a1 * SST + a2 * SSS if model == 3 else (a1 * SST if model == 1 else a2 * SSS)
    return carbonate

## finding the years that are in both datasets
vikingYears = vikingExpertAnoms['year'] if season else vikingAnnualAnoms['year']
d18OYears = d18OAnoms['year']

intersect = np.intersect1d(vikingYears, d18OYears)

## only keeping the overlapping years
vikingFiltered = vikingExpertAnoms.sel(year = intersect) if season else vikingAnnualAnoms.sel(year = intersect)
d18OFiltered = d18OAnoms[d18OAnoms['year'].isin(intersect)]

d18OXRArray = xr.DataArray(
    d18OFiltered['d18OAnoms'].values,
    coords={'year': d18OFiltered['year'].values},
    dims='year',
    name='d18OAnoms'
)

## merge (based on the year)
merged = vikingFiltered.copy()
merged['d18OAnoms'] = d18OXRArray 
df = merged.to_dataframe().reset_index()

## computing the pseudocarbonate for each year
if {'year', 'temp', 'salt'}.issubset(df.columns):
    pseudocarbonateData = []
    for _, row in df.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['temp'],
            SSS=row['salt'])
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

plt.suptitle('Seguin', fontsize = 16, fontweight = 'bold')
method = "Williams et al. Method (Expert Season)" if season else "Williams et al. Method (Annual Season)"
modelType = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + modelType)
plt.legend()
plt.grid(True)
plt.show()

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
nrmse = np.sqrt(((0 - filter['pseudocarb']) ** 2).mean())
print("NRMSE:", nrmse.item())