## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import os
import argparse
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from isleOxyIso import d18OData
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

## method to establish an expert season (oct-sep)
def getExpertYear(time):
    return time.year + int(time.month >= 10)

## building the pseudocarbonate
def pseudocarbonate(SST, SSS, ISO, avgTemp, avgSalt, avgIso):
    ## using the grossman and ku equation (specific to the gulf of maine)
    if (model == 1):
        if(isotope):
            carbonate = ((20.6 - SST)/4.34) + (avgIso - 0.27)
        else:
            carbonate = ((20.6 - SST)/4.34) +  ((0.5 * avgSalt -17.3) - 0.27)
    elif (model == 2):
        if(isotope):
            carbonate = ((20.6 - avgTemp)/4.34) + (ISO - 0.27)
        else:
            carbonate = ((20.6 - avgTemp)/4.34) + ((0.5 * SSS -17.3) - 0.27)
    else:
        if(isotope):
            carbonate = ((20.6 - SST)/4.34) + (ISO - 0.27)
        else:
            carbonate = ((20.6 - SST)/4.34) + ((0.5 * SSS -17.3) - 0.27)
    return carbonate

## loading in the data
dsTemp = xr.open_dataset("./iCESM/selections/tempISLEAUHAUT.nc")
dsSaline = xr.open_dataset("./iCESM/selections/saltISLEAUHAUT.nc")
dsIso = xr.open_dataset("./iCESM/selections/isoISLEAUHAUT.nc")

## fixing the n/a values with forward fill
dsTemp = dsTemp.where(dsTemp['TEMP'] != 0.0)
dsTemp['TEMP'] = dsTemp['TEMP'].ffill('z_t', limit=None)
dsSaline = dsSaline.where(dsSaline['SALT'] != 0.0)
dsSaline['SALT'] = dsSaline['SALT'].ffill('z_t', limit=None)
dsIso = dsIso.where(dsIso['R18O'] != 0.0)
dsIso['R18O'] = dsIso['R18O'].ffill('z_t', limit=None)

## getting just the month and year
print("Extracting month and year...")
dsTemp['month'] = dsTemp['time'].dt.month
dsTemp['year'] = dsTemp['time'].dt.year

dsSaline['month'] = dsSaline['time'].dt.month
dsSaline['year'] = dsSaline['time'].dt.year

dsIso['month'] = dsIso['time'].dt.month
dsIso['year'] = dsIso['time'].dt.year

## calculating the expert years
expertTemp = xr.apply_ufunc(getExpertYear, dsTemp['time'], vectorize=True)
expertSaline = xr.apply_ufunc(getExpertYear, dsSaline['time'], vectorize=True)
expertIso = xr.apply_ufunc(getExpertYear, dsSaline['time'], vectorize=True)

## assigning the new columns the appropriate coordinates
dsTemp = dsTemp.assign_coords(expertYear=expertTemp)
dsSaline = dsSaline.assign_coords(expertYear=expertSaline)
dsIso = dsIso.assign_coords(expertYear=expertIso)

dsTemp = dsTemp.assign_coords(year=dsTemp['time'].dt.year)
dsSaline = dsSaline.assign_coords(year=dsSaline['time'].dt.year)
dsIso = dsIso.assign_coords(year=dsIso['time'].dt.year)

dsTemp = dsTemp.assign_coords(month=dsTemp['time'].dt.month)
dsSaline = dsSaline.assign_coords(month=dsSaline['time'].dt.month)
dsIso = dsIso.assign_coords(month=dsIso['time'].dt.month)

## averaging over space and selecting a specific depth
spatialMeanTemp = dsTemp.mean(dim=['nlat', 'nlon'])
spatialMeanTemp = spatialMeanTemp.sel(z_t = 30000, method = 'nearest')
spatialMeanSaline = dsSaline.mean(dim=['nlat', 'nlon'])
spatialMeanSaline = spatialMeanSaline.sel(z_t = 30000, method = 'nearest')
spatialMeansIso = dsIso.mean(dim=['nlat', 'nlon'])
spatialMeansIso = spatialMeansIso.sel(z_t = 30000, method = 'nearest')

## getting the mean for each overall year
print("Computing means...")
iCESMTempAnnual = spatialMeanTemp.groupby('year').mean('time')
iCESMSalineAnnual = spatialMeanSaline.groupby('year').mean('time')
iCESMIsoAnnual = spatialMeansIso.groupby('year').mean('time')

iCESMTempExpert = spatialMeanTemp.groupby('expertYear').mean('time')
iCESMSalineExpert = spatialMeanSaline.groupby('expertYear').mean('time')
iCESMIsoExpert = spatialMeansIso.groupby('expertYear').mean('time')

## removing the first and last years from the expert dataset
yearsValid = iCESMTempExpert['expertYear'].values[1:-1]
iCESMTempExpert = iCESMTempExpert.where(iCESMTempExpert['expertYear'].isin(yearsValid), drop=True)
iCESMSalineExpert = iCESMSalineExpert.where(iCESMSalineExpert['expertYear'].isin(yearsValid), drop=True)
iCESMIsoExpert = iCESMIsoExpert.where(iCESMIsoExpert['expertYear'].isin(yearsValid), drop=True)

## combining the temperature and salinity results
print("Combining the results...")
resultValues = xr.Dataset()
resultValues['temp'] = iCESMTempExpert['TEMP'] if season else iCESMTempAnnual['TEMP']
resultValues['salt'] = iCESMSalineExpert['SALT'] if season else iCESMSalineAnnual['SALT']
resultValues['iso'] = iCESMIsoExpert['R18O'] if season else iCESMIsoAnnual['R18O']
resultValues['avgTemp'] = iCESMTempExpert['TEMP'].mean() if season else iCESMTempExpert['TEMP'].mean()
resultValues['avgSalt'] = iCESMSalineExpert['SALT'].mean() if season else iCESMSalineExpert['SALT'].mean()
resultValues['avgIso'] = iCESMIsoExpert['R18O'].mean() if season else iCESMIsoExpert['R18O'].mean()

## finding the years that are in both datasets
iCESMYears = iCESMTempExpert['expertYear'] if season else iCESMTempAnnual['year']
d18OYears = d18OData['year']
intersect = np.intersect1d(iCESMYears, d18OYears)

iCESMFiltered = resultValues.sel(expertYear = intersect) if season else resultValues.sel(year = intersect)
d18OFiltered = d18OData[d18OData['year'].isin(intersect)]

if season:
    iCESMFiltered = iCESMFiltered.rename({'expertYear': 'year'})

d18OXRArray = xr.DataArray(
    d18OFiltered['isleAuHautIso'].values,
    coords={'year': d18OFiltered['year'].values},
    dims='year',
    name='d18OData'
)

merged = iCESMFiltered.copy()
merged['d18OData'] = d18OXRArray 
df = merged.to_dataframe().reset_index()

## computing the pseudocarbonate for each year
if {'year', 'temp', 'salt', 'iso'}.issubset(df.columns):
    pseudocarbonateData = []

    for _, row in df.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['temp'],
            SSS=row['salt'],
            ISO=row['iso'],
            avgTemp=row['avgTemp'],
            avgSalt=row['avgSalt'],
            avgIso=row['avgIso'])
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

filepath = "./figures/icesm"
if isotope:
    figname = "isleAuHaut_iCESM_GKM_M" + str(model) + "(I)_" + ("EXP" if season else "ANN") + ".png"
else:
    figname = "isleAuHaut_iCESM_GKM_M" + str(model) + "(S)_" + ("EXP" if season else "ANN") + ".png"
filename = os.path.join(filepath, figname)

plt.suptitle('Isle Au Haut', fontsize = 16, fontweight = 'bold')
method = "Grossman and Ku Method (Expert Season)" if season else "Grossman and Ku Method (Annual Season)"
if isotope:
    modelType = "Temperature + Isotopes" if model == 3 else ("Temperature Only" if model == 1 else "Isotopes Only")
else:
    modelType = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + modelType)
plt.legend()
plt.grid(True)
plt.savefig(filename)


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
nrmse = np.sqrt(((0 - filter['observed']) ** 2).mean())
print("NRMSE:", nrmse.item())

## saving the results to an excel file
file = "psmREUStats.xlsx"
site = "Isle Au Haut"
equation = "GKM"
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
