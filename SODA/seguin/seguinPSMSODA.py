## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import numpy as np
from seguinAnnualAnomalies import sodaAnnualAnoms
from seguinExpertAnomalies import sodaExpertAnoms
from seguinOxyIso import d18OAnoms

latVector = pd.read_csv('./map_data/latitudes.csv')
lonVector = pd.read_csv('./map_data/longitudes.csv')
regionMask = pd.read_csv('./map_data/REGION_MASK.csv')

def pseudocarbonate(lat, lon, SST, SSS, d18O=-1, species="default", data_to_use=2, verbose=False):
    ## define a1 and a2 based on the region (north atlantic)
    a1 = 0.22
    a2 = 0.97002 * 0.55

    ## calculating pseudocarbonate value
    carbonate = a1 * SST + (d18O if d18O != -1 else a2 * SSS)
    return carbonate

## finding the years that are in both datasets
intersect = set(sodaExpertAnoms['year']).intersection(set(d18OAnoms['year']))

## only keeping the overlapping years
sodaFiltered = sodaExpertAnoms[sodaExpertAnoms['year'].isin(intersect)]
d18OFiltered = d18OAnoms[d18OAnoms['year'].isin(intersect)]

## merge on inner join (based on the year)
merged = pd.merge(sodaFiltered, d18OFiltered, on='year', how='inner')

if {'year', 'tempAnoms', 'saltAnoms'}.issubset(merged.columns):
    ## using dummy latitude/longitude
    lat, lon = (360-74.0868), 38.2268

    ## computing the pseudocarbonate for each year
    pseudocarbonateData = []

    for _, row in merged.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            lat, lon,
            SST=row['tempAnoms'],
            SSS=row['saltAnoms'])
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

