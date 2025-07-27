## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import numpy as np
from isleAnnualAnomalies import iCESMAnnualAnoms
from isleExpertAnomalies import iCESMExpertAnoms
from isleOxyIso import d18OAnoms

latVector = pd.read_csv('./map_data/latitudes.csv')
lonVector = pd.read_csv('./map_data/longitudes.csv')
regionMask = pd.read_csv('./map_data/REGION_MASK.csv')

def pseudocarbonate(SST, SSS, d18O=-1, species="default", data_to_use=2, verbose=False):
    ## define a1 and a2 based on the region (north atlantic)
    a1 = 0.22
    a2 = 0.97002 * 0.55

    ## calculating pseudocarbonate value
    carbonate = a1 * SST + (d18O if d18O != -1 else a2 * SSS)
    return carbonate

## finding the years that are in both datasets
iCESMYears = iCESMExpertAnoms['year']
d18OYears = d18OAnoms['year']

intersect = np.intersect1d(iCESMYears, d18OYears)

iCESMFiltered = iCESMExpertAnoms.sel(year = intersect)
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
plt.plot(data['year'], data['d18OAnoms'], label='d18OAnoms', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')

plt.xlabel('Time')
plt.ylabel('Anomaly Value')
plt.title('Isle Au Haut - d18O-carb and d18O-pseudo Over Time')
plt.legend()
plt.grid(True)

plt.show()

