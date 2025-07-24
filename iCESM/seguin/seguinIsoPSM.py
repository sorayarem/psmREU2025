## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import numpy as np
from seguinIsoAnomalies import iCESMAnnualAnoms
from seguinOxyIso import d18OAnoms

latVector = pd.read_csv('./map_data/latitudes.csv')
lonVector = pd.read_csv('./map_data/longitudes.csv')
regionMask = pd.read_csv('./map_data/REGION_MASK.csv')

def pseudocarbonate(SST, ISO, d18O=-1, species="default", data_to_use=2, verbose=False):
    ## define a1 and a2 based on the region (north atlantic)
    a1 = 0.22
    a2 = 0.97002

    ## calculating pseudocarbonate value
    carbonate = a1 * SST + a2 * ISO
    return carbonate

## finding the years that are in both datasets
iCESMYears = iCESMAnnualAnoms['year']
d18OYears = d18OAnoms['year']

intersect = np.intersect1d(iCESMYears, d18OYears)

iCESMFiltered = iCESMAnnualAnoms.sel(year = intersect)
d18OFiltered = d18OAnoms[d18OAnoms['year'].isin(intersect)]

d18OXRArray = xr.DataArray(
    d18OFiltered['d18OAnoms'].values,
    coords={'year': d18OFiltered['year'].values},
    dims='year',
    name='d18OAnoms'
)

merged = iCESMFiltered.copy()
merged['d18OAnoms'] = d18OXRArray 
df = merged.to_dataframe().reset_index()

if {'year', 'temp', 'iso'}.issubset(df.columns):
    ## computing the pseudocarbonate for each year
    pseudocarbonateData = []

    for _, row in df.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['temp'],
            ISO=row['iso'])
        pseudocarbonateData.append(pseudoCarbonateValue)

    ## converting to a data frame
    merged['pseudocarbonate'] = pseudocarbonateData
    data = merged
else:
    print("Missing required columns in overlapping_df")

import pandas as pd
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(data['year'], data['d18OAnoms'], label='d18OAnoms', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')

plt.xlabel('Time')
plt.ylabel('Anomaly Value')
plt.title('Seguin - d18O-carb and d18O-pseudo Over Time')
plt.legend()
plt.grid(True)

plt.show()

