## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import numpy as np
from jonesportOxyIso import d18OData

def pseudocarbonate(SST, SSS, species="default", data_to_use=2, verbose=False):
    ## define a1 and a2 based on the region (north atlantic)
    sw = (0.5 * SSS -17.3)

    ## calculating pseudocarbonate value
    carbonate = ((20.6 - SST)/4.34) + (sw - 0.27)

    return carbonate

dsTemp = xr.open_dataset("./VIKING20X/selections/tempJONESPORT.nc")
dsSaline = xr.open_dataset("./VIKING20X/selections/saltJONESPORT.nc")

## getting just the month and year
print("Extracting month and year...")
dsTemp['year'] = dsTemp['time_counter'].dt.year
dsSaline['year'] = dsSaline['time_counter'].dt.year

dsTemp = dsTemp.assign_coords(year=dsTemp['time_counter'].dt.year)
dsSaline = dsSaline.assign_coords(year=dsSaline['time_counter'].dt.year)

spatialMeanTemp = dsTemp.mean(dim=['y', 'x'])
spatialMeanTemp = spatialMeanTemp.sel(deptht = 0, method = 'nearest')
spatialMeanSaline = dsSaline.mean(dim=['y', 'x'])
spatialMeanSaline = spatialMeanSaline.sel(deptht = 0, method = 'nearest')

print("Computing annual anomalies...")
annualTemp = spatialMeanTemp.groupby('year').mean('time_counter')
annualSaline = spatialMeanSaline.groupby('year').mean('time_counter')

print("Combining the results...")
resultAnomalies = xr.Dataset()
resultAnomalies['temp'] = annualTemp['votemper']
resultAnomalies['salt'] = annualSaline['vosaline']

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
##plt.plot(data['year'], data['d18OData'], label='d18OAnoms', linestyle='-', color='#008080')
##plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')
plt.scatter(data['d18OData'], data['pseudocarbonate'], label='d18OAnoms', color='#008080')
plt.xlabel('Time')
plt.ylabel('Anomaly Value')
plt.title('Jonesport - d18O-carb and d18O-pseudo Over Time')
plt.legend()
plt.grid(True)

plt.show()

