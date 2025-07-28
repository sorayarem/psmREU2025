## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from longIslandOxyIso import d18OData
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

## setting the seasonal preference (F:Annual; T:Expert)
season = False

## setting the model preference (1: Temperature; 2:Salinity, 3:Both)
model = 3

## method to establish an expert season (oct-sep)
def getExpertYear(time):
    time = pd.Timestamp(time)
    return time.year + int(time.month >= 10)

## building the pseudocarbonate
def pseudocarbonate(SST, SSS):
    ## using the grossman and ku equation (specific to the gulf of maine)
    temp = SST
    sw = (0.5 * SSS -17.3)

    ## calculating pseudocarbonate value
    carbonate = ((20.6 - temp)/4.34) + (sw - 0.27) if model == 3 else (((20.6 - temp)/4.34) - 0.27) if model == 1 else ((20.6/4.34) + (sw - 0.27))
    return carbonate

## loading in the data
dsTemp = xr.open_dataset("./GLORYS/selections/tempLONGISLAND.nc")
dsSaline = xr.open_dataset("./GLORYS/selections/saltLONGISLAND.nc")

## getting just the month and year
print("Extracting month and year...")
dsTemp['month'] = dsTemp['time'].dt.month
dsTemp['year'] = dsTemp['time'].dt.year

dsSaline['month'] = dsSaline['time'].dt.month
dsSaline['year'] = dsSaline['time'].dt.year

## calculating the expert years
expertTemp = xr.apply_ufunc(getExpertYear, dsTemp['time'], vectorize=True)
expertSaline = xr.apply_ufunc(getExpertYear, dsSaline['time'], vectorize=True)

## assigning the new columns the appropriate coordinates
dsTemp = dsTemp.assign_coords(expertYear=expertTemp)
dsSaline = dsSaline.assign_coords(expertYear=expertSaline)

dsTemp = dsTemp.assign_coords(year=dsTemp['time'].dt.year)
dsSaline = dsSaline.assign_coords(year=dsSaline['time'].dt.year)

dsTemp = dsTemp.assign_coords(month=dsTemp['time'].dt.month)
dsSaline = dsSaline.assign_coords(month=dsSaline['time'].dt.month)

## averaging over space and selecting a specific depth
spatialMeanTemp = dsTemp.mean(dim=['latitude', 'longitude'])
spatialMeanTemp = spatialMeanTemp.sel(depth = 0, method = 'nearest')
spatialMeanSaline = dsSaline.mean(dim=['latitude', 'longitude'])
spatialMeanSaline = spatialMeanSaline.sel(depth = 0, method = 'nearest')

## getting the mean for each overall year
print("Computing means...")
glorysTempAnnual = spatialMeanTemp.groupby('year').mean('time')
glorysSalineAnnual = spatialMeanSaline.groupby('year').mean('time')

glorysTempExpert = spatialMeanTemp.groupby('expertYear').mean('time')
glorysSalineExpert = spatialMeanSaline.groupby('expertYear').mean('time')

## removing the first and last years from the expert dataset
yearsValid = glorysTempExpert['expertYear'].values[1:-1]
glorysTempExpert = glorysTempExpert.where(glorysTempExpert['expertYear'].isin(yearsValid), drop=True)
glorysSalineExpert = glorysSalineExpert.where(glorysSalineExpert['expertYear'].isin(yearsValid), drop=True)

## combining the temperature and salinity results
print("Combining the results...")
resultAnomalies = xr.Dataset()
resultAnomalies['temp'] = glorysTempExpert['thetao'] if season else glorysTempAnnual['thetao']
resultAnomalies['salt'] = glorysSalineExpert['so'] if season else glorysSalineAnnual['so']

## finding the years that are in both datasets
iCESMYears = glorysTempExpert['expertYear'] if season else glorysTempAnnual['year']
d18OYears = d18OData['year']

intersect = np.intersect1d(iCESMYears, d18OYears)

glorysFiltered = resultAnomalies.sel(expertYear = intersect) if season else resultAnomalies.sel(year = intersect)
d18OFiltered = d18OData[d18OData['year'].isin(intersect)]

if season:
    glorysFiltered = glorysFiltered.rename({'expertYear': 'year'})

d18OXRArray = xr.DataArray(
    d18OFiltered['longIslandIso'].values,
    coords={'year': d18OFiltered['year'].values},
    dims='year',
    name='d18OData'
)

merged = glorysFiltered.copy()
merged['d18OData'] = d18OXRArray 
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
plt.plot(data['year'], data['d18OData'], label='shell record', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')
plt.xlabel('Year')
plt.ylabel('Value')

## plotting the correlation
##plt.scatter(data['d18OData'], data['pseudocarbonate'], label='d18OAnoms', color='#008080')

plt.suptitle('Long Island', fontsize = 16, fontweight = 'bold')
method = "Grossman and Ku Method (Expert Season)" if season else "Grossman and Ku Method (Annual Season)"
model = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + model)
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
