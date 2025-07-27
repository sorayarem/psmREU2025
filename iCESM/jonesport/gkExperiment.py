## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import numpy as np
from jonesportOxyIso import d18OData

def pseudocarbonate(SST, SSS, species="default", data_to_use=2, verbose=False):
    ## define a1 and a2 based on the region (north atlantic)
    temp = SST
    sw = (0.5 * SSS -17.3)

    ## calculating pseudocarbonate value
    carbonate = ((20.6 - temp)/4.34) + (sw - 0.27)

    return carbonate

dsTemp = xr.open_dataset("./iCESM/selections/tempJONESPORT.nc")
dsSaline = xr.open_dataset("./iCESM/selections/saltJONESPORT.nc")

## getting just the month and year
print("Extracting month and year...")
dsTemp['year'] = dsTemp['time'].dt.year
dsSaline['year'] = dsSaline['time'].dt.year

dsTemp = dsTemp.assign_coords(year=dsTemp['time'].dt.year)
dsSaline = dsSaline.assign_coords(year=dsSaline['time'].dt.year)

spatialMeanTemp = dsTemp.mean(dim=['nlat', 'nlon'])
spatialMeanTemp = spatialMeanTemp.sel(z_t = 80, method = 'nearest')
spatialMeanSaline = dsSaline.mean(dim=['nlat', 'nlon'])
spatialMeanSaline = spatialMeanSaline.sel(z_t = 80, method = 'nearest')

print("Computing annual anomalies...")
annualTemp = spatialMeanTemp.groupby('year').mean('time')
annualSaline = spatialMeanSaline.groupby('year').mean('time')

print("Combining the results...")
resultAnomalies = xr.Dataset()
resultAnomalies['temp'] = annualTemp['TEMP']
resultAnomalies['salt'] = annualSaline['SALT']

## finding the years that are in both datasets
iCESMYears = annualTemp['year']
d18OYears = d18OData['year']

intersect = np.intersect1d(iCESMYears, d18OYears)

iCESMFiltered = resultAnomalies.sel(year = intersect)
d18OFiltered = d18OData[d18OData['year'].isin(intersect)]

d18OXRArray = xr.DataArray(
    d18OFiltered['jonesportIso'].values,
    coords={'year': d18OFiltered['year'].values},
    dims='year',
    name='d18OData'
)

merged = iCESMFiltered.copy()
merged['d18OData'] = d18OXRArray 
df = merged.to_dataframe().reset_index()

if {'year', 'temp', 'salt'}.issubset(df.columns):
    ## computing the pseudocarbonate for each year
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

import pandas as pd
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(data['year'], data['d18OData'], label='d18OAnoms', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')

plt.xlabel('Time')
plt.ylabel('Anomaly Value')
plt.title('Jonesport - d18O-carb and d18O-pseudo Over Time')
plt.legend()
plt.grid(True)

plt.show()

