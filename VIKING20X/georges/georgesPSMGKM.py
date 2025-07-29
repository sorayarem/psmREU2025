## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import os
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from georgesOxyIso import d18OData
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

## setting the seasonal preference (F:Annual; T:Expert)
season = 1

## setting the model preference (1: Temperature; 2:Salinity, 3:Both)
model = 3

## method to establish an expert season (oct-sep)
def getExpertYear(time):
    time = pd.Timestamp(time)
    return time.year + int(time.month >= 10)

## building the pseudocarbonate
def pseudocarbonate(SST, SSS, avgTemp, avgSalt):
    ## using the grossman and ku equation (specific to the gulf of maine)
    temp = avgTemp if model == 2 else SST
    sw = (0.5 * avgSalt -17.3) if model == 1 else (0.5 * SSS -17.3)

    ## calculating pseudocarbonate value
    carbonate = ((20.6 - temp)/4.34) + (sw - 0.27)
    return carbonate

## loading in the data
dsTemp = xr.open_dataset("./VIKING20X/selections/tempGEORGES.nc")
dsTemp = dsTemp.where(dsTemp['votemper'] != 0.0)
dsTemp['votemper'] = dsTemp['votemper'].ffill('deptht', limit=None)
dsSaline = xr.open_dataset("./VIKING20X/selections/saltGEORGES.nc")
dsSaline = dsSaline.where(dsSaline['vosaline'] != 0.0)
dsSaline['vosaline'] = dsSaline['vosaline'].ffill('deptht', limit=None)

## getting just the month and year
print("Extracting month and year...")
dsTemp['month'] = dsTemp['time_counter'].dt.month
dsTemp['year'] = dsTemp['time_counter'].dt.year

dsSaline['month'] = dsSaline['time_counter'].dt.month
dsSaline['year'] = dsSaline['time_counter'].dt.year

## calculating the expert years
expertTemp = xr.apply_ufunc(getExpertYear, dsTemp['time_counter'], vectorize=True)
expertSaline = xr.apply_ufunc(getExpertYear, dsSaline['time_counter'], vectorize=True)

## assigning the new columns the appropriate coordinates
dsTemp = dsTemp.assign_coords(expertYear=expertTemp)
dsSaline = dsSaline.assign_coords(expertYear=expertSaline)

dsTemp = dsTemp.assign_coords(year=dsTemp['time_counter'].dt.year)
dsSaline = dsSaline.assign_coords(year=dsSaline['time_counter'].dt.year)

dsTemp = dsTemp.assign_coords(month=dsTemp['time_counter'].dt.month)
dsSaline = dsSaline.assign_coords(month=dsSaline['time_counter'].dt.month)

## averaging over space and selecting a specific depth
spatialMeanTemp = dsTemp.mean(dim=['y', 'x'])
spatialMeanTemp = spatialMeanTemp.sel(deptht = 1136.922, method = 'nearest')
spatialMeanSaline = dsSaline.mean(dim=['y', 'x'])
spatialMeanSaline = spatialMeanSaline.sel(deptht = 1136.922, method = 'nearest')

## getting the mean for each overall year
print("Computing means...")
vikingTempAnnual = spatialMeanTemp.groupby('year').mean('time_counter')
vikingSalineAnnual = spatialMeanSaline.groupby('year').mean('time_counter')

vikingTempExpert = spatialMeanTemp.groupby('expertYear').mean('time_counter')
vikingSalineExpert = spatialMeanSaline.groupby('expertYear').mean('time_counter')

## removing the first and last years from the expert dataset
yearsValid = vikingTempExpert['expertYear'].values[1:-1]
vikingTempExpert = vikingTempExpert.where(vikingTempExpert['expertYear'].isin(yearsValid), drop=True)
vikingSalineExpert = vikingSalineExpert.where(vikingSalineExpert['expertYear'].isin(yearsValid), drop=True)

## combining the temperature and salinity results
print("Combining the results...")
resultAnomalies = xr.Dataset()
resultAnomalies['temp'] = vikingTempExpert['votemper'] if season else vikingTempAnnual['votemper']
resultAnomalies['salt'] = vikingSalineExpert['vosaline'] if season else vikingSalineAnnual['vosaline']
resultAnomalies['avgTemp'] = vikingTempExpert['votemper'].mean() if season else vikingTempAnnual['votemper'].mean()
resultAnomalies['avgSalt'] = vikingSalineExpert['vosaline'].mean() if season else vikingSalineAnnual['vosaline'].mean()

## finding the years that are in both datasets
iCESMYears = vikingTempExpert['expertYear'] if season else vikingTempAnnual['year']
d18OYears = d18OData['year']

intersect = np.intersect1d(iCESMYears, d18OYears)

vikingFiltered = resultAnomalies.sel(expertYear = intersect) if season else resultAnomalies.sel(year = intersect)
d18OFiltered = d18OData[d18OData['year'].isin(intersect)]

if season:
    vikingFiltered = vikingFiltered.rename({'expertYear': 'year'})

d18OXRArray = xr.DataArray(
    d18OFiltered['georgesIso'].values,
    coords={'year': d18OFiltered['year'].values},
    dims='year',
    name='d18OData'
)

merged = vikingFiltered.copy()
merged['d18OData'] = d18OXRArray 
df = merged.to_dataframe().reset_index()

## computing the pseudocarbonate for each year
if {'year', 'temp', 'salt', 'avgTemp', 'avgSalt'}.issubset(df.columns):
    pseudocarbonateData = []

    for _, row in df.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['temp'],
            SSS=row['salt'],
            avgTemp=row['avgTemp'],
            avgSalt=row['avgSalt'])
        pseudocarbonateData.append(pseudoCarbonateValue)

    ## converting to a data frame
    merged['pseudocarbonate'] = pseudocarbonateData
    data = merged
else:
    print("Missing required columns in overlapping_df")

## plotting the results of the PSM
plt.figure(figsize=(12, 6))

## plotting the timeseries
plt.plot(data['year'], data['d18OData'], label='shell record', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')
plt.xlabel('Year')
plt.ylabel('Value')

## plotting the correlation
##plt.scatter(data['d18OData'], data['pseudocarbonate'], label='d18OAnoms', color='#008080')

plt.suptitle('Georges Bank', fontsize = 16, fontweight = 'bold')
method = "Grossman and Ku Method (Expert Season)" if season else "Grossman and Ku Method (Annual Season)"
modelType = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + modelType)
plt.legend()
plt.grid(True)
plt.show()

# creating the merged data frame
df = pd.DataFrame({ 'year': data['year'], 'observed': data['d18OData'], 'pseudocarb': data['pseudocarbonate']})

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

## saving the results to an excel file
file = "psmREUStats.xlsx"
site = "Georges Bank"
equation = "GKM"
data = "VIKING20X"
season = "Expert" if season else "Annual"
method = "Both" if model == 3 else ("Temperature" if model == 1 else "Salinity")

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